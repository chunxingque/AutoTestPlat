# -*- coding: utf-8 -*-

from celery import shared_task

from .web_auto.DatabaseApi import AutoDatabase
from .web_auto.SeleniumApi import SeleniumApi


@shared_task
def task__start_case_selenium(case_id: int, browser: str="chrome",incognito: bool=True,headless=False,window_size: str= None, grid_url: str = None,run_step: int = 0, *args, **kwargs):
    """启用测试用例"""
    # 默认用例执行结果为1成功
    case_result = 1
    auto_sql = AutoDatabase()
    case_steps = auto_sql.get_case_step(case_id,run_step)
    if not case_steps:
        return f'没有找到case_id({case_id})用例步骤!'
    
    auto_sql.init_step_result(case_id)
    
    # 导入模块
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    
    with SeleniumApi(browser=browser,incognito=incognito,headless=headless,window_size=window_size,grid_url=grid_url) as api:
        for step in case_steps:
            try:
                api.main_action(action=step['action'],
                                 find_method=step['find_method'],
                                 find_value=step['find_value'],
                                input_value=step['input_value'])
                
                auto_sql.set_step_result(step['id'],1)
            except NoSuchElementException as e:
                run_log = '未查找到元素,请检查元素定位方法与查找值是否正确！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                
                break
            except TimeoutException as e:
                run_log = '页面加载超时,请检查页面是否正常！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                break
            except Exception as e:
                run_log = '未知错误,请检查日志！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                break
    
    auto_sql.set_case_result(case_id, case_result)
    return f'case_id({case_id})用例执行完成!'


@shared_task
def task__start_case_pw(case_id: int, browser: str="chrome",headless=False,window_size: str= None, grid_url: str = None,run_step: int = 0,*args, **kwargs):
    # 默认用例执行结果为1成功
    case_result = 1
    run_log = ''
    
    auto_sql = AutoDatabase()
    case_steps = auto_sql.get_case_step(case_id,run_step)
    if not case_steps:
        print('没有找到对应的测试步骤!')
        return None
    
    auto_sql.init_step_result(case_id)
    
    # 导入模块
    from .web_auto.PlaywrightApi import PlaywrightApi, NoSuchElementException
    from playwright.sync_api import TimeoutError
    
    with PlaywrightApi(browser=browser,headless=headless,window_size=window_size,grid_url=grid_url) as api:
        for step in case_steps:
            try:
                api.main_action(action=step['action'],
                                 find_method=step['find_method'],
                                 find_value=step['find_value'],
                                input_value=step['input_value'])
                
                auto_sql.set_step_result(step['id'],1)
            except NoSuchElementException as e:
                run_log = '未查找到元素,请检查元素定位方法与查找值是否正确！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                
                print(f'用例步骤ID({step["id"]})运行失败,退出执行！！')
                break
            except TimeoutError as e:
                run_log = '页面加载超时,请检查页面是否正常！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                print(f'用例步骤ID({step["id"]})运行失败,退出执行！！')
                break
            except Exception as e:
                run_log = '未知错误,请检查日志！'
                auto_sql.set_step_result(step['id'],2,run_log)
                case_result = 2
                print(e)
                print(f'用例步骤ID({step["id"]})运行失败,退出执行！！')
                break
    
    auto_sql.set_case_result(case_id, case_result)
    return f'case_id({case_id})用例执行完成!'




