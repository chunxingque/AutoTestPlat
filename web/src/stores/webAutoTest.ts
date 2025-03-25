import { defineStore } from 'pinia';


export const useWebAutoTest = defineStore('webAutoTest', {
	state: () => ({
        runCaseParam: {
            browser: 'chrome',
            incognito: false,
            headless: false,
            window_size: "",
            grid_url: "",
            run_step: 0,
        },
        action: [
            {
                value: "webpage",
                label: "网页操作",
                children: [
                    {
                        value: "webpage_open",
                        label: "打开网页"
                    },
                    {
                        value: "webpage_forward",
                        label: "前进"
                    },
                    {
                        value: "webpage_back",
                        label: "后退"
                    },
                    {
                        value: "webpage_refresh",
                        label: "刷新"
                    },
                    {
                        value: "webpage_window",
                        label: "切换窗口"
                    }
                ]
            },
            {
                value: "mouse",
                label: "鼠标操作",
                children: [
                    {
                        value: "click",
                        label: "单击(左)"
                    },
                    {
                        value: "right_click",
                        label: "单击(右)"
                    },
                    {
                        value: "double_click",
                        label: "双击"
                    },
                    {
                        value: "hover",
                        label: "悬停"
                    },
                    {
                        value: "mouse_move_click",
                        label: "移动点击"
                    },
                    {
                        value: "mouse_scroll",
                        label: "鼠标滚动"
                    },
                ]
            },
            {
                value: "input", 
                label: "输入操作",
                children: [
                    {
                        value: "text_input", 
                        label: "文本输入"
                    },
                    {
                        value: "keyboard_input",
                        label: "键盘输入"
                    }
                ]
            },
            {
                value: "sleep", 
                label: "等待时间"
            },
    
        ],
        find_method: [
            {
                value: "find_element_by_id",
                label: "by_id"
            },
            {
                value: "find_element_by_xpath",
                label: "by_xpath"
            },
            {
                value: "find_element_by_css_selector",
                label: "by_css_selector"
            },
            {
                value: "find_element_by_class",
                label: "by_class"
            },
            {
                value: "find_element_by_name",
                label: "by_name"
            },
        ],
        brower: [
            {
                value: "chrome",
                label: "chrome"
            }
        ],
        window_size: [
            {
                value: "",
                label: "默认大小"
            },
            {
                value: "max",
                label: "窗口最大化"
            },
            {
                value: "1280x720",
                label: "1280x720"
            },
            {
                value: "1024x768",
                label: "1024x768"
            },          
            {
                value: "1920x1080",
                label: "1920x1080"
            }
        ],
        keyboard: ['NULL','HELP','BACKSPACE','TAB','CLEAR','RETURN','ENTER','SHIFT','LEFT_SHIFT','CONTROL','LEFT_CONTROL','ALT','LEFT_ALT','PAUSE','ESCAPE','SPACE','PAGE_UP','PAGE_DOWN','END','HOME','LEFT','ARROW_LEFT','UP','ARROW_UP','RIGHT','ARROW_RIGHT','DOWN','ARROW_DOWN','INSERT','DELETE','SEMICOLON','EQUALS','NUMPAD0','NUMPAD1','NUMPAD2','NUMPAD3','NUMPAD4','NUMPAD5','NUMPAD6','NUMPAD7','NUMPAD8','NUMPAD9','MULTIPLY','ADD','SEPARATOR','SEPARATOR','DECIMAL','DIVIDE','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12'],
	    webpage_window: [
            {
                value: "0", 
                label: "第一个"
            },
            {
                value: "-1", 
                label: "最后一个"
            },
            {
                value: "1", 
                label: "上一个"
            },
            {
                value: "2", 
                label: "下一个"
            },
        ]
    })
});
