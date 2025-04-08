import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options

        
class SeleniumApi():
    def __init__(self,browser: str="chrome",incognito: bool=True,headless=False,window_size: str= None, grid_url: str = None) -> None:
        """_summary_

        Args:
            browser (str, optional): _description_. Defaults to chrome.
            incognito (bool, optional): 无痕模式. Defaults to False. 
            headless (bool, optional): 无界面模式. Defaults to False.
            window_size (str, optional): 界面大小. Defaults to None. example: max,min,1920x1080
        """
        
        self.driver = None
        self.browser = browser
        self.incognito = incognito
        self.headless = headless
        self.window_size = window_size
        self.grid_url = grid_url.strip('/') if grid_url else None
    

    def set_chrome_driver(self):
        self.chrome_options = Options()
        if self.incognito:
            self.chrome_options.add_argument('--incognito')
        if self.headless:
            self.chrome_options.add_argument('--headless')
        
        if self.grid_url:
            self.driver = webdriver.Remote(command_executor=self.grid_url,options=self.chrome_options)
        else:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        
        self.driver.implicitly_wait(10)
        if self.window_size:
            if self.window_size == 'max':
                self.driver.maximize_window()
            elif self.window_size == 'min':
                self.driver.minimize_window()
            elif 'x' in self.window_size:
                width,height = self.window_size.split('x')
                self.driver.set_window_size(width, height)
        
    def set_driver(self):
        if not self.driver:
            if self.browser == 'chrome':
                self.set_chrome_driver()
            else:
                self.set_chrome_driver()

    def find_element(self, find_method, find_value) -> WebElement:
        """查找单个元素"""
        if find_method == 'find_element_by_id':
            element = self.driver.find_element(By.ID,find_value)
        elif find_method == 'find_element_by_class':
            element = self.driver.find_element(By.CLASS_NAME,find_value)
        elif find_method == 'find_element_by_xpath':
            element = self.driver.find_element(By.XPATH,find_value)
        elif find_method == 'find_element_by_css_selector':
            element = self.driver.find_element(By.CSS_SELECTOR,find_value)
        elif find_method == 'find_element_by_name':
            element = self.driver.find_element(By.NAME,find_value)
        else:
            print("find method is not defined")
            return None
        return element
    
    def keyboard_action(self, action, find_method: str=None,find_value: str=None, input: str=None):
        """键盘操作"""
        if action == 'text_input':
            element = self.find_element(find_method,find_value)
            element.clear()
            element.send_keys(input)
        elif action == 'keyboard_input':
            if find_value and find_method:
                element = self.find_element(find_method,find_value)
                key_value = self.set_keys_attr(input)
                element.send_keys(key_value)
            else:
                key_value = self.set_keys_attr(input)
                ActionChains(self.driver).send_keys(key_value).perform()
    
    def mouse_action(self, element: WebElement, action, input: str=None):
        """鼠标操作"""
        if action == 'click':
            element.click()
        elif action == 'double_click':
           ActionChains(self.driver).double_click(element).perform()
        elif action == 'right_click':
            ActionChains(self.driver).context_click(element).perform()
        elif action == 'hover':
            ActionChains(self.driver).move_to_element(element).perform()
    
    def mouse_action_other(self, action, find_method: str=None,find_value: str=None, input: str=None):
        """鼠标其他操作"""
        if action == 'mouse_move_click':
            coordinate = input.split(',')
            coordinate_x = int(coordinate[0])
            coordinate_y = int(coordinate[1])
            
            script = """
                var marker = document.createElement('div');
                marker.style.position = 'absolute';
                marker.style.left = arguments[0] + 'px';
                marker.style.top = arguments[1] + 'px';
                marker.style.width = '20px';
                marker.style.height = '20px';
                marker.style.backgroundColor = 'red';
                marker.style.borderRadius = '50%';
                marker.style.zIndex = '9999'; 
                document.body.appendChild(marker);
                // 2 秒后删除标记
                setTimeout(function() {
                    marker.remove();
                }, 2000);
            """
            
            if find_value and find_method:
                element = self.find_element(find_method,find_value)
                # 左上角偏移点击
                left_top_x = element.location['x']
                left_top_y = element.location['y']
                self.driver.execute_script(script, left_top_x + coordinate_x, left_top_y + coordinate_y)
                action = ActionBuilder(self.driver)
                action.pointer_action.move_to_location(left_top_x + coordinate_x, left_top_y + coordinate_y).click()
                action.perform()
                
            else:
                self.driver.execute_script(script,coordinate_x,coordinate_y)                
                action = ActionBuilder(self.driver)
                action.pointer_action.move_to_location(coordinate_x,coordinate_y).click()
                action.perform()
        elif action == 'mouse_scroll':
            try:
                delta_y = int(input)
                if find_value and find_method:
                    element = self.find_element(find_method,find_value)
                    ActionChains(self.driver).scroll_to_element(element=element).perform()
                    scroll_origin = ScrollOrigin.from_element(element)
                    if delta_y != 0:
                        ActionChains(self.driver)\
                            .scroll_from_origin(scroll_origin, 0, delta_y)\
                            .perform()
                else:
                    ActionChains(self.driver).scroll_by_amount(0, delta_y).perform()                    
            except ValueError as e:
                print('请设置鼠标滚动值为数字！！')
    
    def webpage_action(self, action, input: str=None):
        """网页操作"""
        if action == 'webpage_open':
            self.driver.get(input)
        elif action == 'webpage_forward':
            self.driver.forward()
        elif action == 'webpage_back':
            self.driver.back()
        elif action == 'webpage_refresh':
            self.driver.refresh()
        elif action == 'webpage_window':
            # 窗口标签页操作
            # 注意: 点击链接跳转到一个新窗口时,driver还是旧的窗口，需要手动切换到新窗口
            # flag: -1: 最后一个标签页 0: 第一个标签页, 1: 上一个标签页, 2: 下一个标签页
            flag = int(input)
            if flag == -1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
            elif flag == 0:
                self.driver.switch_to.window(self.driver.window_handles[0])
            elif flag == 1:
                prev_tab_index = (self.driver.window_handles.index(self.driver.current_window_handle)) - 1
                if prev_tab_index >= 0:
                    self.driver.switch_to.window(self.driver.window_handles[prev_tab_index])
                else:
                    print("已经是第一个标签页")
            elif flag == 2:
                next_tab_index = (self.driver.window_handles.index(self.driver.current_window_handle)) + 1
                if next_tab_index < len(self.driver.window_handles):
                    self.driver.switch_to.window(self.driver.window_handles[next_tab_index])
                else:
                    print("已经是最后一个标签页")
                
    
    def set_keys_attr(self, key):
        """设置键盘属性值"""
        if hasattr(Keys,key):
            return getattr(Keys,key)
        else:
            return getattr(Keys,'NULL')

    def main_action(self, action, find_method,find_value,input_value):
        """网页的所有操作"""
        mouse_action = ['click','double_click','right_click','hover']
        
        if 'webpage' in action:
            self.webpage_action(action,input_value)
        elif action == 'sleep':
            time.sleep(float(input_value)) 
        elif action in mouse_action:
            element = self.find_element(find_method,find_value)
            self.mouse_action(element,action,input_value) 
        elif 'input' in action:
            self.keyboard_action(action,find_method,find_value,input_value)
        elif 'mouse' in action:
            self.mouse_action_other(action,find_method,find_value,input_value)     
        else:
            print(f'暂不支持"{action}"操作')
        
    def __enter__(self):
        self.set_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    seleniumapi = SeleniumApi()
    print(seleniumapi.set_keys_attr('ENTER'))
    

    
    
    
    
        
        
    



