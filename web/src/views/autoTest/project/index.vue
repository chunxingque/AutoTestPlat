<template>
	<div class="app-container" ref="appContainer">
	  <PropTable
		  :loading="loading"
		  @selection-change="selectionChange"
		  :columns="column"
		  :data="project_data.data"
		  :count="project_data.count"
		  @reset="reset"
		  @onSubmit="onSubmit"
		  @size-change="handleSizeChange"
		  @pageChange="handlePageChange"
	  >
		<template v-slot:btn>
		  <div style="display: flex; justify-content: flex-end">
			<el-button type="primary" @click="project_add"
			><el-icon><plus /></el-icon> 添加</el-button
			>
			<el-button type="danger" @click="batchDelete"
			><el-icon><delete /></el-icon>删除</el-button
			>
		  </div>
		</template>
		<template v-slot:result="scope">
		 <span>
            <a-tag v-if="scope.row.result == 0" > 未执行 </a-tag>
            <a-tag v-else-if="scope.row.result == 1" style="color: #2ecc71"> 执行成功 </a-tag>
            <a-tag v-else-if="scope.row.result == 2" style="color: #ffa200"> 执行失败 </a-tag>
          </span>
		</template>
		<template v-slot:operation="scope">
		  <el-button type="primary" size="small" icon="Edit" @click="project_edit(scope.row.id)">
			编辑
		  </el-button>
		  <el-button @click="del_project(scope.row.id)" type="danger" size="small" icon="Delete">
			删除
		  </el-button>
		</template>
	  </PropTable>
  
	  <el-dialog v-model="Dialog.visible" :title="Dialog.title" destroy-on-close  style="max-width: 600px; width: 40%; padding: 16px 16px 0px 16px">
			<ProjectInput  @onFinish="onFinish" :id="Dialog.id" :mode="Dialog.mode" ></ProjectInput>
	  </el-dialog>
	</div>
</template>

<script lang="ts" setup name="projectPage">
import {ref, reactive, onMounted, nextTick} from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router';

import PropTable from '/@/components/table/PropTable/index.vue'
import ProjectInput from './components/ProjectInput.vue';
import * as api from './api'


const router = useRouter();
const loading = ref(true)
const appContainer = ref(null)

// 项目数据
const project_data = reactive({
	param: {
		page: 1,
		page_size: 10,
		name: '',
	},
	count: 0,
	data: [],
})

const column = [
	{ type: 'selection', width: 60 ,fixed: 'left'},
	{ name: 'name', label: '项目名称', inSearch: true, valueType: 'input',width: 200 },
	{ name: 'description', label: '项目描述' },
	{ name: 'operation', slot: true, fixed: 'right', width: 300,label: '操作'  },
]
// 表格选择
const selectObj = ref([])


// 获取项目列表
const getProject = () => {
	api.GetProjectList(project_data.param).then((res) => {
		project_data.data = res.data;
		project_data.count = res.count;
	}).catch((err) => {
		console.log(err);
	})
}

// 获取项目列表并等待后加载数据
const getProjectWait = (delay=false) => {
	if (delay) {
		loading.value = true
		setTimeout(() => {
			getProject();
		}, 500)
	} else {
		loading.value = true
		getProject();
	}
	setTimeout(() => {
		loading.value = false	
	}, 500)
}


// 添加与编辑变量
const Dialog = reactive({
	visible: false,
	id: 0,
	title: '',
	mode: 0,
})
// 添加项目事件
const project_add = () => {
	Dialog.title = '项目新增'
	Dialog.mode = 0
	Dialog.visible = true
}

// 编辑项目事件
const project_edit = (id: number) => {
	Dialog.id = id
	Dialog.title = '项目编辑'
	Dialog.mode = 1
	Dialog.visible = true
}

// 添加与编辑项目完成事件
const onFinish = () => {
	getProjectWait(true);
	Dialog.visible = false
}

// 搜索重置事件
const reset = () => {
	ElMessage.success('触发重置方法')
	project_data.param.name = ''
	getProjectWait();
}

const onSubmit = (val) => {
	// console.log('val===', val)
	ElMessage.success('触发查询方法')
	project_data.param.name = val.name
	getProjectWait();
}

// 删除测试项目与步骤
const del_project = (id: number) => {
	ElMessageBox.confirm('你确定要删除当前项吗?', '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	})
	.then(() => {
		api.DelProject(id)
		.then((res) => {
			ElMessage.success('删除成功')
			getProjectWait();
		})
		.catch((err) => {
			ElMessage.error(err)
		})
	})
	.catch(() => {})
}

const batchDelete = () => {
	if (!selectObj.value.length) {
		return ElMessage.error('未选中任何行')
	}
	ElMessageBox.confirm('你确定要删除选中项吗?', '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	})
	.then(() => {
		for (let i = 0; i < selectObj.value.length; i++) {
			var id: number = selectObj.value[i].id;
			api.DelProject(id)
			.then((res) => {
				ElMessage.success('删除成功')
				getProjectWait();
			})
			.catch((err) => {
				ElMessage.error(err)
			})
		}
	})
	.catch(() => {})
}

const selectionChange = (val) => {
	selectObj.value = val
}

// 分页大小
const handleSizeChange = (val: number) => {
	project_data.param.page_size = val;
	getProjectWait();
}

// 切换分页
const handlePageChange = (val: number) => {
	project_data.param.page = val;
	getProjectWait();
}

onMounted(() => {
	getProject();
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
  