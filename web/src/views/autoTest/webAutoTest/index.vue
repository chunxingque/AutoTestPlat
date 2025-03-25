<template>
	<div class="app-container" ref="appContainer">
	  <PropTable
		  :loading="loading"
		  @selection-change="selectionChange"
		  :columns="column"
		  :data="case_data.data"
		  :count="case_data.count"
		  @reset="reset"
		  @onSubmit="onSubmit"
		  @size-change="handleSizeChange"
		  @pageChange="handlePageChange"
	  >
	    
		<template v-slot:btn>
		  <div style="display: flex; justify-content: flex-end">
			<el-button type="primary" @click="case_add"
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
			<el-button type="success" size="small" icon="Edit" @click="open_web_case_scene(scope.row.id)">
				用例场景
			</el-button>

			<el-dropdown style="margin-left: 5px">
				<el-button type="primary" size="small">
					用例操作<el-icon class="el-icon--right"><arrow-down /></el-icon>
				</el-button>
				<template #dropdown>
					<el-dropdown-menu>
						<el-dropdown-item @click="case_edit(scope.row.id)" style="color: #109c27;">编辑</el-dropdown-item>
						<el-dropdown-item @click="case_copy(scope.row.id)" style="color: #5352ed;">复制</el-dropdown-item>
						<el-dropdown-item @click="del_case(scope.row.id)" style="color: red;">删除</el-dropdown-item>
					</el-dropdown-menu>
				</template>
			</el-dropdown>
		</template>
	  </PropTable>
  
	  <el-dialog v-model="Dialog.visible" :title="Dialog.title" destroy-on-close style="max-width: 600px; width: 40%;padding: 16px 16px 0px 16px">
			<WebCaseView  @onFinish="onFinish" :id="Dialog.id" :mode="Dialog.mode" ></WebCaseView>
	  </el-dialog>
	</div>
</template>

<script lang="ts" setup name="CasePage">
import {ref, reactive, onMounted, nextTick,watch} from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router';

import PropTable from '/@/components/table/PropTable/index.vue'
import WebCaseView from './components/WebCaseView.vue';
import { GetCaseList,DelCaseStep} from './api';
import { useProjectConfig } from '/@/stores/projectConfig'

const router = useRouter();
const loading = ref(true)
const appContainer = ref(null)

const projectConfig = useProjectConfig()

// 用例数据
const case_data = reactive({
	param: {
		page: 1,
		page_size: 10,
		name: '',
		result: '',
		project_id: '' as number | string,
	},
	count: 0,
	data: [],
})


const column = [
	{ type: 'selection', width: 60 ,fixed: 'left'},
	{ name: 'name', label: '用例名称', inSearch: true, valueType: 'input', width: 200 },
	{ name: 'description', label: '用例描述', min_width: 200 },
	{ name: 'project_name', label: '用例项目', width: 200, valueType: 'input' },
	{
		name: 'result',
		label: '用例结果',
		slot: true,
		inSearch: true,
		options: [
		{
			value: 0,
			label: '未执行',
		},
		{
			value: 1,
			label: '执行成功',
		},
		{
			value: 2,
			label: '执行失败',
		},
		],
		valueType: 'select',
		width: 150,
	},
	// {name: 'tester', label: '执行用户', valueType: 'input',width: 200},
	{name: 'run_time', label: '执行时间', valueType: 'input',width: 200},
	{name: 'create_time', label: '创建时间', valueType: 'input',width: 200},
	{name: 'operation', slot: true, fixed: 'right', width: 250,label: '操作'  },
]


// 表格选择
const selectObj = ref([])


// 获取用例列表
const getCase = () => {
	GetCaseList(case_data.param).then((res) => {
		case_data.data = res.results
		case_data.count = res.count
	}).catch((err) => {
		console.log(err);
	})
}

// 获取用例列表并等待
const getCaseWait = (delay=false) => {
	if (delay) {
		loading.value = true
		setTimeout(() => {
			getCase();
		}, 500)
	} else {
		loading.value = true
		getCase();
	}
	setTimeout(() => {
		loading.value = false	
	}, 500)
}

// 监听项目id,项目id变化,重新获取用例列表
watch(() => projectConfig.id, (newVal) => {
	if (typeof newVal == 'number' ) {
		case_data.param.project_id = newVal;
	} else {
		case_data.param.project_id = ''
	}
	getCaseWait();
})

// 用例场景事件
const open_web_case_scene = (case_id: number) => {
	router.push({ path: "/webcasescene", query: { case_id } })
}


// 添加与编辑变量
const Dialog = reactive({
	visible: false,
	id: 0,
	title: '',
	mode: 0,
})
// 添加用例事件
const case_add = () => {
	Dialog.title = '用例新增'
	Dialog.mode = 0;
	Dialog.visible = true
}

// 编辑用例事件
const case_edit = (id: number) => {
	Dialog.id = id
	Dialog.title = '用例编辑'
	Dialog.mode = 1;
	Dialog.visible = true
}

// 复制用例事件
const case_copy = (id: number) => {
	Dialog.id = id
	Dialog.title = '用例复制'
	Dialog.mode = 2;
	Dialog.visible = true
}

// 添加与编辑用例完成事件
const onFinish = () => {
	getCaseWait(true);
	Dialog.visible = false
}


const reset = () => {
	case_data.param.name = ''
	case_data.param.result = ''
	ElMessage.success('触发重置方法');
	getCaseWait();
}

const onSubmit = (val) => {
	// console.log('val===', val)
	ElMessage.success('触发查询方法')
	case_data.param.name = val.name
	case_data.param.result = val.result
	case_data.param.project_id = projectConfig.id
	getCaseWait();
}

// 删除测试用例与步骤
const del_case = (id: number) => {
	ElMessageBox.confirm('你确定要删除当前项吗?', '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	})
	.then(() => {
		DelCaseStep(id)
		.then((res) => {
			ElMessage.success('删除成功')
			getCaseWait(true);
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
			DelCaseStep(id)
			.then((res) => {
				ElMessage.success('删除成功')
				loading.value = true
				setTimeout(() => {
					loading.value = false
					getCase();
				}, 500)
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
	case_data.param.page_size = val;
	getCaseWait();
}

// 切换分页
const handlePageChange = (val: number) => {
	case_data.param.page = val;
	getCaseWait();
}

onMounted(() => {
	if (typeof projectConfig.id == 'number') {
		case_data.param.project_id = projectConfig.id
	}
	
	getCase();
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
  