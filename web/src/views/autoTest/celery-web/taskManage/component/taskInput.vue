<template>
<div>
    <el-form ref="taskFormRef" :rules="rules" :model="taskForm" label-width="120px"
                label-position="left">
        <el-row>
            <el-col>
                <el-form-item label="任务名称" required prop="name">
                    <el-input v-model="taskForm.name"/>
                </el-form-item>
            </el-col>
            <el-col>
                <el-form-item label="任务类型" required prop="task">
                    <el-select v-model="taskForm.task" @focus="loadTaskList" class="w-full">
                        <el-option v-for="item in selectedTaskList" :key="item.value"
                                    :label="item.label"
                                    :value="item.value"/>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col>
                <el-form-item label="任务参数" prop="kwargs">
                    <el-input v-model="taskForm.kwargs"/>
                </el-form-item>
            </el-col>
            <el-col>
                <el-form-item label="调度器类型" required prop="schedule">
                    <el-radio-group v-model="taskForm.schedule_type" @change="schedule_type_change">
                        <el-radio-button label="CrontabSchedule" :value="0" />
                        <el-radio-button label="IntervalSchedule" :value="1" />
                        <el-radio-button label="ClockedSchedule" :value="2" />
                    </el-radio-group>

                </el-form-item>
                
                <div v-show="taskForm.schedule_type==0">
                    <el-form-item label="调度器" required>
                        <el-select v-model="taskForm.schedule" @focus="loadIntervalScheduleList"
                                    class="w-full" clearable>
                            <el-option v-for="item in intervalScheduleList" :key="item.value"
                                        :value="item.id"
                                        :label="`every: ${item.every}; period: ${item.period}`"
                            >
        
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
                <div v-show="taskForm.schedule_type==1">
                    <el-form-item label="调度器" required>
                        <el-select v-model="taskForm.schedule" @focus="loadCrontabScheduleList"
                                    class="w-full" clearable>
                            <el-option v-for="item in crontabScheduleList" :key="item.value"
                                        :value="item.id"
                                        :label="`${item.minute} ${item.hour} ${item.day_of_month} ${item.month_of_year}  ${item.day_of_week}`"
                            >
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
                <div v-show="taskForm.schedule_type==2">
                    <el-form-item label="调度器" required>
                        <el-select v-model="taskForm.schedule" @focus="loadClockedScheduleList"
                                    class="w-full" clearable>
                            <el-option v-for="item in clockedScheduleList" :key="item.value"
                                        :value="item.id"
                                        :label="item.clocked_time"
                            >
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col>
            <el-col>
                <el-form-item label="是否启用" required prop="enabled">
                    <el-switch v-model="taskForm.enabled"/>
                </el-form-item>
            </el-col>
            <el-col>
                <el-form-item label="只运行一次" required prop="one_off">
                    <el-switch v-model="taskForm.one_off"/>
                    
                </el-form-item>
                <p>调度器需要先在调度管理中添加;调度器类型为Clocked时,只运行一次选项必须选择 </p>
                
            </el-col>
        </el-row>
        <div style="display: flex;justify-content: end; align-items: center;">
            <el-button type="primary" @click="sumit_form(taskFormRef)"  style="margin-right: 10px;">保 存</el-button>
        </div>
    </el-form>
</div>

</template>

<script setup lang="ts">
import { ref,reactive,onMounted,watch } from 'vue';
import {FormInstance, FormRules} from "element-plus";

import {errorMessage, successMessage} from '/@/utils/message';
import * as api from '../api'

const emit = defineEmits(['onFinish']);
// 0: 新增 1：修改 2：复制
const props = defineProps({
    id: {
        type: Number,
        default: 0,
    },
    mode: {
        type: Number,
        default: 0,
    },
    kwargs: {
        type: String,
        default: '',
    },
    name: {
        type: String,
        default: '',
    }
});


const taskFormRef = ref<FormInstance>()

const taskForm = reactive({
    name: '',
    task: '',
    schedule_type: 0,//0 IntervalSchedule 1 CrontabSchedule
    schedule: '',
    enabled: true,
    one_off: false,
    kwargs: '{}',
})

interface taskFormRules {
    name: string,
    task: string,
    schedule: string,
    one_off: boolean,
    enabled: boolean,

}

const rules = reactive<FormRules<taskFormRules>>({
    name: [
        {required: true, message: '请输入任务名称', trigger: 'blur'},
    ], task: [
        {required: true, message: '请选择一个任务', trigger: 'blur'},
    ], schedule: [
        {required: true, message: '请选择schedule', trigger: 'blur'},
    ], enabled: [
        {required: true, message: '请选择状态', trigger: 'blur'},
    ],
})

// 切换调度器时,重置schedule
const schedule_type_change = () =>{
    taskForm.schedule = '';
    if(taskForm.schedule_type == 2) {
        taskForm.one_off = true;
    } else {
        taskForm.one_off = false;
    }
}


/*
* 加载任务列表
* */
const selectedTaskList = ref({}) as any;
const intervalScheduleList = ref({}) as any;
const crontabScheduleList = ref({}) as any;
const clockedScheduleList = ref({}) as any;

const loadTaskList = () => {
    api.getBackendTaskList({}).then((res: APIResponseData) => {
        if (res.code === 2000) {
            selectedTaskList.value = res.data
        }
    })
}

const loadIntervalScheduleList = () => {
    api.getIntervalScheduleList({}).then((res: APIResponseData) => {
        if (res.code === 2000) {
            intervalScheduleList.value = res.data
        }
    })
}

const loadCrontabScheduleList = () => {
    api.getCrontabScheduleList({}).then((res: APIResponseData) => {
        if (res.code === 2000) {
            crontabScheduleList.value = res.data
            
        }
    })
}

const loadClockedScheduleList = () => {
    api.getClockedScheduleList({}).then((res: APIResponseData) => {
        if (res.code === 2000) {
            clockedScheduleList.value = res.data
        }
    })
}



const addTask = async () => {
    api.AddTask(taskForm).then((res: APIResponseData) => {
        if (res.code === 2000) {
            successMessage('定时任务添加成功!');
            emit('onFinish');
        }
    })
}

// 调度器数据处理
const schedule_type_handle = () =>{
    if (taskForm.schedule_type == 0) {
        taskForm.interval = taskForm.schedule
        taskForm.crontab = null
        taskForm.clocked = null
    } else if (taskForm.schedule_type == 1) {
        taskForm.crontab = taskForm.schedule
        taskForm.interval = null
        taskForm.clocked = null
    } else if (taskForm.schedule_type == 2) {
        taskForm.clocked = taskForm.schedule
        taskForm.interval = null
        taskForm.crontab = null
    }
} 


const editTask = async () => {
    schedule_type_handle();
    api.EditTask(taskForm).then((res: APIResponseData) => {
        if (res.code === 2000) {
            successMessage('定时任务编辑成功!');
            emit('onFinish');
        }
    })
}

const sumit_form = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate( async (valid, fields) => {
    if (valid) {
        if (props.mode == 1) {
            await editTask();
        }  else {
            await addTask();
        }
    } else {
      console.log('error submit!', fields)
    }
  })
}

// 获取任务详情
const getTask = async (id: number) => {
    api.GetTask(id).then((res: APIResponseData) => {
        if (res.code === 2000) {
            var re_data = res.data;
            for (const key in re_data) {
                if (re_data['crontab']){
                    taskForm.schedule_type = 1
                    taskForm.schedule = re_data['crontab']
                } else if (re_data['interval']){
                    taskForm.schedule_type = 0
                    taskForm.schedule = re_data['interval']
                } else if (re_data['clocked']){
                    taskForm.schedule_type = 2
                    taskForm.schedule = re_data['clocked']
                }
                taskForm[key] = re_data[key]
            }
        }
    })
}



onMounted(() => {
    if (props.kwargs){
        console.log(props.kwargs);
        taskForm.kwargs = props.kwargs;
    }
    if (props.name){
        taskForm.name = props.name;
    }
    if (props.mode == 1){
        getTask(props.id);
        loadTaskList();
        loadIntervalScheduleList();
        loadCrontabScheduleList();
        loadClockedScheduleList();
    }
    

})

</script>