<template>
	<div class="app-container" ref="appContainer">
	  <PropTable
		  :loading="loading"
		  @selection-change="selectionChange"
		  :columns="column"
		  :data="task_data.data"
		  :count="task_data.count"
		  @reset="reset"
		  @onSubmit="onSubmit"
		  @size-change="handleSizeChange"
		  @pageChange="handlePageChange"
	  >
		<template v-slot:btn>
		  <div style="display: flex; justify-content: flex-end">
			<el-button type="primary" @click="addTaskShow"
			><el-icon><plus /></el-icon> 添加
            </el-button>
		  </div>
		</template>
		<template v-slot:enabled="scope">
            <div>
                <el-popconfirm width="180" confirm-button-text="确定" @confirm="setTaskStatus(scope.row)"
                                cancel-button-text="取消"
                                :title="scope.row.enabled ? '确认停用该任务？' : '确认启用该任务？'">
                    <template #reference>
                        <el-tag v-if="scope.row.enabled == true" type="success" effect="dark">已启用</el-tag>
                        <el-tag v-else type="danger" effect="dark">已停用</el-tag>
                    </template>
                </el-popconfirm>
            </div>
		</template>
        <template v-slot:schedule_type="scope">
            <div>
                <el-tag v-if="scope.row.schedule_type == 0" type='success'>interval</el-tag>
                <el-tag v-else-if="scope.row.schedule_type == 1" type='success'>crontab</el-tag>
				<el-tag v-else-if="scope.row.schedule_type == 2" type='success'>clocked</el-tag>
                <el-tag v-else type="success" effect="dark">未知</el-tag>
            </div>
		</template>
		<template v-slot:one_off="scope">
            <div>
                <el-tag v-if="scope.row.one_off" type='success'>是</el-tag>
				<el-tag v-else type='danger'>否</el-tag>
            </div>
		</template>
       
		<template v-slot:operation="scope">
		  <el-button type="primary" size="small" icon="Edit" @click="editTaskShow(scope.row.id)">
			编辑
		  </el-button>
		  <el-button @click="delTask(scope.row.id)" type="danger" size="small" icon="Delete">
			删除
		  </el-button>
		</template>
	  </PropTable>
  
        <el-dialog v-model="taskDialog.visible" :title="taskDialog.title" destroy-on-close  width="40%" style="padding: 16px 16px 0px 16px">
            <taskInput 
                :mode="taskDialog.mode"
                :id="taskDialog.id"
                @onFinish="taskOnFinish" >
            </taskInput>
        </el-dialog>
	</div>
</template>

<script lang="ts" setup name="taskManage">
import {ref, reactive, onMounted, nextTick,toRaw} from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import PropTable from '/@/components/table/PropTable/index.vue'
import taskInput from './component/taskInput.vue'
import * as api from './api'


const loading = ref(true)
const appContainer = ref(null)

// 项目数据
const task_data = reactive({
	param: {
		page: 1,
		page_size: 10,
		name: '',
        enabled: null as boolean | null,
	},
	count: 0,
	data: [],
})


const column = [
	{ type: 'selection', width: 60 ,fixed: 'left'},
	{ name: 'name', label: '任务名称', inSearch: true, valueType: 'input',width: 200 },
	{ name: 'task_type', label: '任务类型',width: 150},
    { name: 'kwargs', label: '任务参数' },
    { name: 'schedule_type', label: '调度器',slot: true,width: 100},
    { name: 'schedule', label: '调度器参数',width: 200},
	{ name: 'one_off', label: '只运行一次',width: 100,slot: true},
    { name: 'enabled', label: '任务状态',width: 100,
        slot: true,
		inSearch: true,
		options: [
		{
			value: false,
			label: '暂停',
		},
		{
			value: true,
			label: '运行',
		},
		],
		valueType: 'select', 
    },
    { name: 'last_run_at', label: '上次运行时间' },
	{ name: 'total_run_count', label: '运行次数' },
	{ name: 'operation', slot: true, fixed: 'right', width: 300,label: '操作'  },
]


// 表格选择
const selectObj = ref([])

// 获取项目列表
const getTaskList = () => {
    api.getTaskList(task_data.param).then((res: APIResponseData) => {
        task_data.data = res.data;
		task_data.count = res.total;
    });
}

// 延迟获取用例项目
const getTaskListWait = () => {
	loading.value = true
	setTimeout(() => {
		loading.value = false
		getTaskList();
	}, 500)
}

// 定时任务添加与编辑
const taskDialog = reactive({
    visible: false,
    title: '定时任务添加',
    mode: 0,
    id: null as number | null
})

const addTaskShow = () => {
    taskDialog.mode = 0;
    taskDialog.visible = true;
}

const editTaskShow = (id: number) => {
    taskDialog.mode = 1;
    taskDialog.id = id;
    taskDialog.title = '定时任务编辑';
    taskDialog.visible = true;
}


const taskOnFinish = () => {
    setTimeout(() => {
        getTaskList();
        taskDialog.visible = false;
    }, 500);
}


const reset = () => {
	task_data.param.name = '';
    task_data.param.enabled = null;
	getTaskList();
	loading.value = true
	setTimeout(() => {
		loading.value = false;
	}, 500)
	ElMessage.success('触发重置方法')
}

const onSubmit = (val) => {
	// console.log('val===', val)
	ElMessage.success('触发查询方法')
	task_data.param.name = val.name;
    task_data.param.enabled = val.enabled;
	getTaskList();
	loading.value = true
	setTimeout(() => {
		loading.value = false
	}, 500)
}

// 删除测试项目与步骤
const delTask = (id: number) => {
	ElMessageBox.confirm('你确定要删除当前任务吗?', '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	})
	.then(() => {
        api.DelTask(id).then((res: APIResponseData) => {
            if (res.code === 2000) {
                ElMessage.success('删除成功')
                loading.value = true
                setTimeout(() => {
                    loading.value = false
                    getTaskList();
                }, 500)
            }
        })
	})
	.catch(() => {})
}

const selectionChange = (val) => {
	selectObj.value = val
}

// 分页大小
const handleSizeChange = (val: number) => {
	task_data.param.page_size = val;
	getTaskListWait();
}

// 切换分页
const handlePageChange = (val: number) => {
	task_data.param.page = val;
	getTaskListWait();
}

/**
 * 设置任务状态
 * @param item 任务
 */

 const setTaskStatus = (item: any) => {
    item.enabled = !item.enabled;
    api.UpdateTask({enabled: item.enabled, id: item.id}).then((res: APIResponseData) => {
        if (res.code === 2000) {
            ElMessage.success(res.msg as string)
            getTaskListWait();
        }
    });

}

onMounted(() => {
	getTaskList();
	nextTick(()=>{
		// let data = appContainer.value.
	})
	setTimeout(() => {
		loading.value = false
	}, 500)
})
</script>
  
<style scoped>
  .app-container{
	flex: 1;
	display: flex;
	width: 100%;
	padding: 16px;
	box-sizing: border-box;
  }

</style>
  