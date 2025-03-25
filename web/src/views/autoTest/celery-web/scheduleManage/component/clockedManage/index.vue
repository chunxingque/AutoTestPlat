<template>
	<div class="app-container" ref="appContainer">
	  <PropTable
		  :loading="loading"
		  @selection-change="selectionChange"
		  :columns="column"
		  :data="clocked_data.data"
		  :count="clocked_data.count"
		  @reset="reset"
		  @onSubmit="onSubmit"
		  @size-change="handleSizeChange"
		  @pageChange="handlePageChange"
	  >
		<template v-slot:btn>
		  <div style="display: flex; justify-content: flex-end">
			<el-button type="primary" @click="clocked_add"
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
		  <el-button type="primary" size="small" icon="Edit" @click="clocked_edit(scope.row.id)">
			编辑
		  </el-button>
		  <el-button @click="del_clocked(scope.row.id)" type="danger" size="small" icon="Delete">
			删除
		  </el-button>
		</template>
	  </PropTable>
  
	  <el-dialog v-model="Dialog.visible" :title="Dialog.title" destroy-on-close  style="max-width: 600px; width: 40%; padding: 16px 16px 0px 16px">
			<ClockedInput  @onFinish="onFinish" :id="Dialog.id" :mode="Dialog.mode" ></ClockedInput>
	  </el-dialog>
	</div>
</template>

<script lang="ts" setup name="clockedManage">
import {ref, reactive, onMounted, nextTick} from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import PropTable from '/@/components/table/PropTable/index.vue'
import ClockedInput from './components/ClockedInput.vue';
import * as api from './api'

const loading = ref(true)
const appContainer = ref(null)

// 时间数据
const clocked_data = reactive({
	param: {
		page: 1,
		page_size: 10,
	},
	count: 0,
	data: [],
})

const column = [
	{ type: 'selection', width: 60 ,fixed: 'left'},
	{ name: 'id', label: 'ID', inSearch: true, valueType: 'input',width: 200 },
	{ name: 'clocked_time', label: '时间' },
	{ name: 'operation', slot: true, fixed: 'right', width: 300,label: '操作'  },
]
// 表格选择
const selectObj = ref([])


// 获取时间列表
const getClocked = () => {
	api.GetClockedList(clocked_data.param).then((res) => {
		clocked_data.data = res.data;
		clocked_data.count = res.count;
	}).catch((err) => {
		console.log(err);
	})
}

// 获取时间列表并等待后加载数据
const getClockedWait = (delay=false) => {
	if (delay) {
		loading.value = true
		setTimeout(() => {
			getClocked();
		}, 500)
	} else {
		loading.value = true
		getClocked();
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
// 添加时间事件
const clocked_add = () => {
	Dialog.title = '时间新增'
	Dialog.mode = 0
	Dialog.visible = true
}

// 编辑时间事件
const clocked_edit = (id: number) => {
	Dialog.id = id
	Dialog.title = '时间编辑'
	Dialog.mode = 1
	Dialog.visible = true
}

// 添加与编辑时间完成事件
const onFinish = () => {
	getClockedWait(true);
	Dialog.visible = false
}

// 搜索重置事件
const reset = () => {
	ElMessage.success('触发重置方法')
	clocked_data.param.name = ''
	getClockedWait();
}

const onSubmit = (val) => {
	// console.log('val===', val)
	ElMessage.success('触发查询方法')
	clocked_data.param.name = val.name
	getClockedWait();
}

// 删除测试时间与步骤
const del_clocked = (id: number) => {
	ElMessageBox.confirm('你确定要删除当前项吗?', '温馨提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
		draggable: true,
	})
	.then(() => {
		api.DelClocked(id)
		.then((res) => {
			ElMessage.success('删除成功')
			getClockedWait();
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
			api.DelClocked(id)
			.then((res) => {
				ElMessage.success('删除成功')
				getClockedWait();
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
	clocked_data.param.page_size = val;
	getClockedWait();
}

// 切换分页
const handlePageChange = (val: number) => {
	clocked_data.param.page = val;
	getClockedWait();
}

onMounted(() => {
	getClocked();
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
  