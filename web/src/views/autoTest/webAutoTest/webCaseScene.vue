<template>
    <div class="app-container">
        <div class="case_layout">
            <el-row style="height: 100%">
                <el-col :span="4" style="display: flex; align-items: center; ">
                    <h2 style="font-size: medium;">用例名称: {{ case_data.name }}</h2>
                </el-col>
                <el-col :span="20" style="display: flex; align-items: center; justify-content: end; padding-right: 15px;">
                    <el-button type="primary" @click="handleRunConfig">运行配置</el-button>
                    <el-button type="success" @click="RunCaseSubmit">运行用例</el-button>
                    <el-button type="success" @click="scheduleRunCaseEvent">定时运行用例</el-button>
                </el-col>
            </el-row>
        </div>
        <div class="case_layout">
            <el-row style="height: 100%">
                <el-col :span="4" style="display: flex; align-items: center; ">
                    <h2 style="font-size: medium;">场景步骤</h2>
                </el-col>
            </el-row>
        </div>
    
        <div class="case_layout" style="overflow: auto; flex-grow: 1; height: 300px;"> 
            <div id="casestep" style="padding: 10px 15px 10px 10px;">
                <div class="step-item" v-for="(step,index) in case_steps" :key="step.id" >
                    <el-row style="height: 100%">
                        <el-col :span="12" style="display: flex; align-items: center;" >
                            <span class="dragitem"> 
                                <svg t="1736236875509" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4379" width="20" height="24"><path d="M256 768.064a64 64 0 1 1-64 64 64 64 0 0 1 64-64z m0-320a64 64 0 1 1-64 64 64 64 0 0 1 64-64z m0-320a64 64 0 1 1-64 64A64 64 0 0 1 256 128z m512 640a64 64 0 1 1-64 64 64 64 0 0 1 64-64z m0-320a64 64 0 1 1-64 64 64 64 0 0 1 64-64z m0-320a64 64 0 1 1-64 64A64 64 0 0 1 768 128z" fill="#585858" p-id="4380"></path></svg>  
                            </span> 
                            <div class="circle-border">{{ step.step_order }}</div> 
                            <span style="margin-left: 10px;font-size: larger;">  {{ step.name }}</span>
                        </el-col>
                        <el-col :span="2" style="display: flex; align-items: center; justify-content: end; ">   
                            
                            <el-popover
                                placement="top-start"
                                :width="250"
                                trigger="hover"
                            >    
                                <template #reference>
                                    <el-button v-if="step.result==1" style="width: 90px; background-color: rgb(135 248 176);"> 执行成功 </el-button>
                                    <el-button v-else-if="step.result==2" style="width: 90px; background-color: rgb(255 115 115);"> 执行失败 </el-button>
                                    <el-button v-else style="width: 90px; background-color: #dcd9d9;"> 未执行 </el-button>
                                </template>
                                <div>
                                    <p>
                                        <span style="font-weight: bold;">执行结果：</span>
                                        <span v-if="step.result==1">成功</span> 
                                        <span v-else-if="step.result==2">失败</span> 
                                        <span v-else >未执行</span> 
                                    </p>
                                    <p>
                                        <span style="font-weight: bold;">执行时间：</span>
                                        <span>{{ step.run_time }}</span>
                                    </p>
                                    <p v-if="step.result==2" >
                                        <span style="font-weight: bold;">错误日志：</span>
                                        <span >{{ step.run_log }}</span>
                                    </p>
                                </div>
                            </el-popover>
                            
                        </el-col>
                        <el-col :span="5" style="display: flex; align-items: center; justify-content: end; ">
                            <el-button @click="stepEditEvent(step.id)"  type="success" plain :icon="Edit">
                                编辑
                            </el-button>
                            <el-button @click="del_web_case_step(step.id,step.step_order)" :icon="Delete" type="danger" plain>
                                删除
                            </el-button>
                        </el-col>
                        <el-col :span="5" style="display: flex; align-items: center; justify-content: end; ">
                            
                            <el-dropdown placement="bottom" @command="handleStepCopy"  style="margin-right: 10px">
                                <span>
                                    复制
                                    <el-icon> <arrow-down /> </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item :command="{ command: 'up', index: index }">向上</el-dropdown-item>
                                        <el-dropdown-item :command="{ command: 'down', index: index }" >向下</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                            <el-dropdown placement="bottom" @command="handleStepInsert"  style="margin-right: 10px">
                                <span>
                                    插入
                                    <el-icon> <arrow-down /> </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item :command="{ command: 'up', index: index }">向上</el-dropdown-item>
                                        <el-dropdown-item :command="{ command: 'down', index: index }" >向下</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>

                            <el-dropdown placement="bottom" @command="handleMove"  style="margin-right: 10px">
                                <span>
                                    移动
                                    <el-icon> <arrow-down /> </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item  :command="{ command: 'up', index: index}" v-if="index !=0" >向上</el-dropdown-item>
                                        <el-dropdown-item :command="{ command: 'down', index: index}" v-if="index != case_steps.length-1">向下</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                             
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
        <div class="case_layout" style="display: flex;justify-content: start;" >
            <el-button type="primary" @click="refresh_web_case_step" style="margin-left: 5px;">刷 新</el-button>
            <el-button type="primary" @click="open_drawer">添加步骤</el-button>
        </div>
        <el-drawer
            v-model="drawer.visible"
            :title="drawer.title"
            direction="rtl"
            size="35%"
            :destroy-on-close="true"
        >
            <CaseStepInput 
                @onFinish="onFinish" 
                :case_id="case_data.id" 
                :step_id="drawer.step_id"
                :step_order="drawer.step_order"
                :mode="drawer.mode" 
            >
            </CaseStepInput>
        </el-drawer>

        <el-dialog v-model="runCaseDialog.visible" :title="runCaseDialog.title" width="40%" style="padding: 16px 16px 0px 16px">
			<el-form 
                :model="webAutoTestStore.runCaseParam" 
                label-width="auto" 
                label-position="top" 
                style="max-width: 100%; padding: 20px"
            >
            <el-row :gutter="20">
                <el-col :span="12">
                    <el-form-item label="浏览器" prop="browser" label-position="top">
                        <el-select v-model="webAutoTestStore.runCaseParam.browser" placeholder="浏览器" >
                            <el-option
                                v-for="item in webAutoTestStore.brower"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            /> 
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="运行界面" prop="headless" label-position="top">
                            <el-select v-model="webAutoTestStore.runCaseParam.headless" placeholder="运行界面" >
                                <el-option
                                    label="有界面"
                                    :value="false"
                                /> 
                                <el-option
                                    label="无界面"
                                    :value="true"
                                /> 
                            </el-select>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="20">
                <el-col :span="12">
                    <el-form-item label="窗口大小" prop="window_size">
                        <el-select v-model="webAutoTestStore.runCaseParam.window_size" placeholder="默认大小" >
                            <el-option
                                v-for="item in webAutoTestStore.window_size"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            /> 
                        </el-select>
                    </el-form-item> 
                </el-col>
                <el-col :span="12">
                    <el-form-item label="运行步数" prop="run_step" label-position="top">
                        <el-input-number v-model="webAutoTestStore.runCaseParam.run_step":min="0" style="width: 100%; "/>
                    </el-form-item>
                </el-col>
            </el-row>
            
            
            <el-form-item label="Selenium Grid地址" prop="grid_url">
                <el-input v-model="webAutoTestStore.runCaseParam.grid_url" placeholder="http://127.0.0.1:4444" />
            </el-form-item>
            <el-form-item label="无痕模式: " prop="incognito" label-position="left">
                        <el-radio-group v-model="webAutoTestStore.runCaseParam.incognito">
                            <el-radio :value="true">是</el-radio>
                            <el-radio :value="false">否</el-radio>
                        </el-radio-group>
            </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer" style="margin-bottom: 10px;">
                    <el-button type="primary" @click="runCaseDialog.visible = false">确 认</el-button>
                </div>
            </template>

        </el-dialog>

        <el-dialog v-model="scheduleRunCaseDialog.visible" :title="scheduleRunCaseDialog.title"  width="40%" style="padding: 16px 16px 0px 16px">
            <taskInput :mode="scheduleRunCaseDialog.mode" :kwargs="scheduleRunCaseDialog.kwargs" :name="case_data.name" @onFinish="scheduleRunOnFinish" ></taskInput>
        </el-dialog>
    </div>
    

</template>

<script lang="ts" setup name="CaseStepPage">
import { ref,reactive,onMounted } from 'vue';
import { useRoute,useRouter } from 'vue-router'
import Sortable from 'sortablejs';
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'

import { GetCase,GetWebStepList,DelWebStep,WebStepOrder,runCaseTask } from './api';
import { CaseStepType } from './types'
import  CaseStepInput from './components/CaseStepInput.vue';
import { useWebAutoTest } from "/@/stores/webAutoTest";
import taskInput from '/@/views/autoTest/celery-web/taskManage/component/taskInput.vue'

const route = useRoute()
const router = useRouter()

const webAutoTestStore = useWebAutoTest();

// 用例基本信息
const case_data = reactive({
    id: 1,
    name: '新建场景',
})

// 用例步骤信息
const case_steps = ref<CaseStepType[]>([]);

// 获取用例基本信息
const get_web_case = () => {
    GetCase(case_data.id).then((res) => {
       case_data.name = res.name;
    }).catch((err) => {
        ElMessage.error('用例不存在!!');
    })
}

// 获取用例所有步骤
const get_web_case_step = () => {
    GetWebStepList(case_data.id).then((res) => {
        case_steps.value = res.results;
    }).catch((err) => {
        ElMessage.error('用例步骤获取失败!!');
    })
}

// 刷新用例步骤信息
const refresh_web_case_step = () => {
    GetWebStepList(case_data.id).then((res) => {
        case_steps.value = res.results;
        ElMessage.success('刷新成功！');
    }).catch((err) => {
        ElMessage.error('用例步骤获取失败!!');
    })
}

// 删除步骤
const del_web_case_step = (id: string,order: number) => {
    console.log(order)
    ElMessageBox.confirm(`你确定要删除步骤${order}吗?`, '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	}).then(() => {
        DelWebStep(id).then((res) => {
            ElMessage.success('删除成功！')
            setTimeout(() => {
                get_web_case_step();
            }, 1000);
        }).catch((err) => {
            ElMessage.error('删除失败！')

        })
    }).catch(() => {
        ElMessage.info('已取消删除')
    })
}



// 拖拽排序功能
const rowDrop = () => {
    const el = document.getElementById("casestep");
    const sorttable = Sortable.create(el, {
        handle: ".dragitem",
        sort: true,
        animation: 150,
        ghostClass: 'sortable-ghost',
        onEnd: (evt: any) => {
            if (evt.newIndex != evt.oldIndex) {
                move_case_step(evt.oldIndex + 1,evt.newIndex + 1);
            }
            
        },
    });
}


//  新建和编辑抽屉组件
const drawer = reactive({
    visible: false,
    title: '新建步骤',
    step_order: 1,
    step_id: '',
    mode: 0,
});

interface DropdownCommandType {
    command: string,
    index: number,
} 

// 添加步骤事件
const open_drawer = () => {
    drawer.step_order = case_steps.value.length + 1;
    drawer.title = '新建步骤' + drawer.step_order;
    drawer.mode = 0;
    drawer.step_id = '';
    drawer.visible = true;
}


// 新建和编辑完成回调函数
const onFinish = () => {
    drawer.visible = false;
    setTimeout(() => {
        get_web_case_step();
    }, 1000);
}


// 复制步骤事件
const handleStepCopy = (command: DropdownCommandType) => {
    var index = command.index;
    var step_order =  case_steps.value[index].step_order as number;
    var step_id = case_steps.value[index].id as string;

    if (command.command == 'up') {
        drawer.step_order = step_order;
    } else if (command.command == 'down') {
        drawer.step_order = step_order + 1;
    }

    drawer.title = '新建步骤' + drawer.step_order;
    drawer.mode = 2;
    drawer.step_id = step_id;
    drawer.visible = true;
}



// 插入步骤事件
const handleStepInsert = (command: DropdownCommandType) => {
    var index = command.index;
    var step_order =  case_steps.value[index].step_order;
    if (command.command == 'up') {
        drawer.step_order = step_order;
    } else if (command.command == 'down') {
        drawer.step_order = step_order + 1;
    }

    drawer.title = '新建步骤' + drawer.step_order;
    drawer.mode = 0;
    drawer.visible = true;
}


// 编辑与删除触发事件处理函数
// const handleCommand = (command: DropdownCommandType) => {
//     var index = command.index;
//     var id = case_steps.value[index].id as string;

//     if (command.command == 'edit') {
//         drawer.step_id = id;
//         drawer.title = '编辑步骤';
//         drawer.mode = 1;
//         drawer.visible = true;
//     } else if (command.command == 'delete') {
//         del_web_case_step(id,case_steps.value[index].name);
//     }
// }

// 编辑事件
const stepEditEvent = (id: string) => {
    drawer.step_id = id;
    drawer.title = '编辑步骤';
    drawer.mode = 1;
    drawer.visible = true;
}

// 移动函数
const move_case_step = (old_order: number,new_order: number) => {
    var data = {
        case_id: case_data.id,
        old_order: old_order,
        new_order: new_order,
    }

    WebStepOrder(data).then((res) => {
        setTimeout(() => {
            get_web_case_step();
            ElMessage.success('移动成功！')
        }, 1000);
    }).catch((err) => {
        console.log(err)
    })
}

// 移动触发事件处理函数
const handleMove = (command: object) => {
    var index = command.index;
    var step_order =  case_steps.value[index].step_order as number;
    if (command.command == 'up') {
        move_case_step(step_order,step_order-1);
    } else if (command.command == 'down') {
        move_case_step(step_order,step_order+1);
    }
}

const runCaseDialog = reactive({
    visible: false,
    title: '运行配置',
})

const handleRunConfig = () => {
    runCaseDialog.visible = true;
}

// 运行用例提交函数
const RunCaseSubmit = () => {
    ElMessageBox.confirm("你确定要运行该测试用例?", '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	}).then(() => {
        var param = {
            case_id: Number(route.query.case_id),
            ...webAutoTestStore.runCaseParam
        }
        runCaseTask(param).
        then((res) => {
            ElMessage.success('用例已提交执行！')
            setTimeout(() => {
                runCaseDialog.visible = false;
            }, 1000);
        }).catch((err) => {
            console.log(err)
        })
    }).catch(() => {
        ElMessage.info('已取消运行')
    })
}

// 定时执行用例
const scheduleRunCaseDialog = reactive({
    visible: false,
    title: '定时运行WebUi用例',
    mode: 0,
    kwargs: '',
})

const scheduleRunCaseEvent = () => {
    var runCaseParam = {
        case_id: Number(route.query.case_id),
        ...webAutoTestStore.runCaseParam
    }
    scheduleRunCaseDialog.mode = 0;
    scheduleRunCaseDialog.kwargs = JSON.stringify(runCaseParam);
    scheduleRunCaseDialog.visible = true;
}

const scheduleRunOnFinish = () => {
    setTimeout(() => {
        scheduleRunCaseDialog.visible = false;
        ElMessage.success('定时任务已提交,请前往任务管理中查看！');
    }, 500);
}

onMounted(() => {
    if (route.query.case_id == undefined) {
        ElMessage.error('case_id不能为空,将返回用例列表界面');
        setTimeout(() => {
            router.push({path: "/uiauto/web"});
        }, 1000);
    } else {
        case_data.id = Number(route.query.case_id);
        get_web_case();
        get_web_case_step();
        rowDrop();
    }
})


</script>

<style scoped>
    .sortable-ghost {
        background-color: #d0d0d0;
        opacity: 0.8;
        border: 2px dashed #000;
    }

    .step-item {
        border-style: solid; 
        border-color: grey;; 
        border-width: 1px; 
        margin: 5px;
        height: 45px;
        width: 100%;
        padding: 5px;
        max-width: 1300px;
    }

    .dragitem {
        cursor: move;
        width: 25px;
    }

    .icon-ele {
    margin: 0 8px 0 auto;
    color: #409eff;
    }
    .case_layout {
        background-color: white; 
        margin: 5px 0px 5px 5px;
        padding: 5px 0px 5px 5px;
    }
    .app-container{
    width: 100%;
    height: 100%;
    padding: 10px 0px 0px 10px;
    box-sizing: border-box;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
   
    }
    .circle-border {
    width: 20px;
    height: 20px;
    border-radius: 50%; /* 设置边框半径为50%，形成圆形 */
    display: flex;
    justify-content: center;
    align-items: center;
    background: #d2d2d2;
    margin-left: 10px;
  }

   .step-result {
        height: 100%;
        width: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        
    }

</style>