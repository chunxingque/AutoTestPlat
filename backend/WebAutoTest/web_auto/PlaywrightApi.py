import time
import os
import sys

from playwright.sync_api import sync_playwright
from playwright._impl._locator import Locator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import KeysMap


class NoSuchElementException(Exception):
    """查找元素异常"""
    pass


class PlaywrightApi():
    def __init__(self,browser: str="chrome",headless=False,window_size: str= None, *args, **kwargs) -> None:
        """_summary_

        Args:
            browser (str, optional): _description_. Defaults to chrome.
            incognito (bool, optional): 无痕模式. Defaults to False. 
            headless (bool, optional): 无界面模式. Defaults to False.
            window_size (str, optional): 界面大小. Defaults to None. example: max,min,1920x1080
        """
        
        self.browser = None
        self.playwright = None
        self.page = None
        self.context = None
        self.browser_type = browser
        self.headless = headless
        self.window_size = window_size

    def set_chrome_browser(self):
        self.playwright = sync_playwright().start()
        
        if not self.window_size:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()  
        else:
            if self.window_size == 'max':
                self.browser = self.playwright.chromium.launch(headless=self.headless,args=['--start-maximized'])
                self.context = self.browser.new_context(no_viewport=True)
                self.page = self.context.new_page()
            elif self.window_size == 'min':
                self.browser = self.playwright.chromium.launch(headless=self.headless,args=['--start-minimized'])
                self.context = self.browser.new_context(no_viewport=True)
                self.page = self.context.new_page()
            elif 'x' in self.window_size:
                self.browser = self.playwright.chromium.launch(headless=self.headless)
                self.context = self.browser.new_context()
                self.page = self.context.new_page()
                width,height = self.window_size.split('x')
                self.page.set_viewport_size({"width": int(width), "height": int(height)})                
            else: 
                self.browser = self.playwright.chromium.launch(headless=self.headless)
                self.context = self.browser.new_context()
                self.page = self.context.new_page()
       
    def set_browser(self):
        if not self.browser:
            if self.browser_type == 'chrome':
                self.set_chrome_browser()
            else:
                self.set_chrome_browser()

    def find_element(self, find_method, find_value) -> Locator  :
        """查找单个元素"""
        if find_method == 'find_element_by_id':
            elements = self.page.locator(f'#{find_value}')
        elif find_method == 'find_element_by_class':
            elements = self.page.locator(f'.{find_value}')
        elif find_method == 'find_element_by_xpath':
            elements = self.page.locator(f'xpath={find_value}')
        elif find_method == 'find_element_by_css_selector':
            elements = self.page.locator(f'css={find_value}')
        elif find_method == 'find_element_by_name':
            elements = self.page.locator(f"[name='{find_value}']")
        else:
            print("find method is not defined")
            return None
        
        if elements.count() > 0:
            element = elements.first
        else:
            raise NoSuchElementException('未查找到元素,请检查元素定位方法与查找值是否正确！')
        return element
    
    def keyboard_action(self, action, find_method: str=None,find_value: str=None, input: str=None):
        """键盘操作"""
        if action == 'text_input':
            element = self.find_element(find_method,find_value)
            element.clear()
            element.fill(input)
        elif action == 'keyboard_input':
            if find_value:
                element = self.find_element(find_method,find_value)
                key = self.map_keys_attr(input)
                if key:
                    element.press(key)
                else:
                    print('key is not defined')
                    element.press("")
    
    def mouse_action(self, element: Locator, action):
        """鼠标操作"""
        if action == 'click':
            element.click()
        elif action == 'double_click':
           element.dblclick()
        elif action == 'right_click':
            element.click(button="right")
        elif action == 'hover':
            element.hover()
    
    def mouse_action_other(self, action, find_method: str=None,find_value: str=None, input: str=None):
        """鼠标其他操作"""
        if action == 'mouse_move_click':
            coordinate = input.split(',')
            coordinate_x = int(coordinate[0])
            coordinate_y = int(coordinate[1])
            
            script = """
            ([coordinate_x,coordinate_y]) => {
                var marker = document.createElement('div');
                marker.style.position = 'absolute';
                marker.style.left = coordinate_x + 'px';
                marker.style.top = coordinate_y + 'px';
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
            }
            """
            
            if find_value:
                element = self.find_element(find_method,find_value)
                bounding_box = element.bounding_box()
                # 获取点击的左上点坐标
                mouse_x = bounding_box['x'] + coordinate_x
                mouse_y = bounding_box['y'] + coordinate_y
                self.page.evaluate(script, [mouse_x, mouse_y])
                self.page.mouse.click(mouse_x, mouse_y)
                
            else:
                self.page.evaluate(script,[coordinate_x,coordinate_y])
                
                self.page.mouse.click(coordinate_x,coordinate_y)
        elif action == 'mouse_scroll':
            delta_y = int(input)
            if find_value:
                element = self.find_element(find_method,find_value)
                element.scroll_into_view_if_needed()
                element.evaluate("window.scrollBy(0, arguments[0])", delta_y)
            else:
                self.page.mouse.wheel(0, delta_y)

    def webpage_action(self, action, input: str=None):
        """网页操作"""
        if action == 'webpage_open':
            self.page.goto(input)
        elif action == 'webpage_forward':
            self.page.go_forward()
        elif action == 'webpage_back':
            self.page.go_back()
        elif action == 'webpage_refresh':
            self.page.reload()
        elif action == 'webpage_window':
            # 窗口标签页操作
            # 注意: 点击链接跳转到一个新窗口时,browser还是旧的窗口，需要手动切换到新窗口
            # flag: -1: 最后一个标签页 0: 第一个标签页, 1: 上一个标签页, 2: 下一个标签页
            flag = int(input)
            pages = self.context.pages
            current_index = pages.index(self.page)
            
            if flag == -1:
                self.page = pages[-1]
                self.page.bring_to_front()
            elif flag == 0:
                self.page = pages[0]
                self.page.bring_to_front()
            elif flag == 1:
                if current_index > 0:
                    self.page = pages[current_index - 1]
                    self.page.bring_to_front()
                else:
                    print('当前是第一个标签页')
            elif flag == 2:
                if current_index < len(pages) - 1:
                    self.page = pages[current_index + 1]
                    self.page.bring_to_front()
                else:
                    print('当前是最后一个标签页')
    
    def map_keys_attr(self, key):
        """映射键盘属性值"""
        if hasattr(KeysMap,key):
            return getattr(KeysMap,key)
        else:
            return getattr(KeysMap,'')

    def main_action(self, action, find_method,find_value,input_value):
        """网页的所有操作"""
        mouse_action = ['click','double_click','right_click','hover']
        
        if 'webpage' in action:
            self.webpage_action(action,input_value)
        elif action == 'sleep':
            time.sleep(float(input_value)) 
        elif action in mouse_action:
            element = self.find_element(find_method,find_value)
            self.mouse_action(element,action) 
        elif 'input' in action:
            self.keyboard_action(action,find_method,find_value,input_value)
        elif 'mouse' in action:
            self.mouse_action_other(action,find_method,find_value,input_value)     
        else:
            print(f'暂不支持"{action}"操作')
        
    def __enter__(self):
        self.set_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

if __name__ == '__main__':
    with PlaywrightApi() as play:
        play.main_action('webpage_open',None,None,'https://www.baidu.com')
        time.sleep(2)
        
    

    
    
    
    
        
        
    



