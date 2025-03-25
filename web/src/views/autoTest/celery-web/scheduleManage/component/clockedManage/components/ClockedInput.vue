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
                <el-form-item label="时间: " prop="clocked_time">
                    <el-date-picker
                    v-model="data_form.clocked_time"
                    type="datetime"
                    placeholder="选择日期时间"
                    format="YYYY-MM-DD HH:mm:ss"
                    value-format="YYYY-MM-DD HH:mm:ss"
                    size="large"
                    />
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
import { ClockedType } from '../types'

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
const rules = reactive<FormRules<ClockedType>>({
    clocked_time: [
    { required: true, message: '请输入时间', trigger: 'blur' },
  ],
});

const data_form = ref<ClockedType>({
  clocked_time: '',
});

// 添加数据api
const add_data = () => {
    api.AddClocked(data_form.value)
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
    api.EditClocked(id,data_form.value)
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
    api.GetClocked(id).then((res) => {
        data_form.value = res;
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