<template>
    <div style="display: flex; flex-direction: column; height: 100%;">
        <div style="height: 93%;">
            <el-form 
                ref="formRef"
                :model="data_form" 
                :rules="rules"
                label-width="auto" 
                label-position="right" 
                style="padding: 10px"
            >
                <el-form-item label="项目名称" prop="name">
                    <el-input v-model="data_form.name" />
                </el-form-item>
                <el-form-item label="项目描述" prop="description">
                    <el-input v-model="data_form.description" />
                </el-form-item>
            </el-form>
        </div>
        <div style="display: flex;justify-content: end;height: 7%; align-items: center;">
            <el-button type="primary" @click="sumit_form(formRef)" style="margin-right: 20px;">保 存</el-button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref,reactive,onMounted } from 'vue';
import { ElMessage,FormInstance,FormRules } from 'element-plus'
import * as api from '../api'
import { ProjectType } from '../types'

// 0: 新增 1：修改 2：复制
const props = defineProps({
    id: {
        type: Number,
        default: 0,
    },
    mode: {
        type: Number,
        default: 0,
    }
});


const emit = defineEmits(['onFinish']);

const formRef = ref<FormInstance>();

// 表单验证规则类型定义
const rules = reactive<FormRules<ProjectStepType>>({
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, message: '字符至少2个及以上', trigger: 'blur' },
  ],
});

const data_form = ref<ProjectType>({
  name: '',
  description: '',
});


// 添加数据api
const add_data = () => {
    api.AddProject(data_form.value)
    .then((res) => {
        ElMessage({
            message: '保存成功',
            type: 'success',
        })
        
    }).catch((err) => {
        console.log(err);
    });
}

// 修改数据api
const edit_data= (id: number) => {
    api.EditProject(id,data_form.value)
    .then((res) => {
        ElMessage({
            message: '保存成功',
            type: 'success',
        })
        
    }).catch((err) => {
        console.log(err);
    });
}

// 表单提交事件处理函数
const sumit_form = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
        if (props.mode == 1) {
            edit_data(props.id)
        }  else {
            add_data()
        }
        emit('onFinish');
    } else {
      console.log('error submit!', fields)
    }
  })
}

// 获取数据api
const  get_data =  (id: number) => {
    api.GetProject(id).then((res) => {
        data_form.value = res.data;
    }).catch((err) => {
        console.log(err);
    })
}

onMounted(() => {
    if (props.mode == 1 || props.mode == 2) {
        get_data(props.id);
    }
})

</script> 