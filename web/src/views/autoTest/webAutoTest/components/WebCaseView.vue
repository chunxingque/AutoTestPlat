<template>
    <div style="display: flex; flex-direction: column; height: 100%;">
        <div style="height: 93%;">
            <el-form 
                ref="formRef"
                :model="data_form" 
                :rules="rules"
                label-width="auto" 
                label-position="right" 
                style="max-width: 600px; padding: 10px"
            >
                <el-form-item label="用例名称" prop="name">
                    <el-input v-model="data_form.name" />
                </el-form-item>
                <el-form-item label="用例项目" prop="project_id">
                     <el-select
                        v-model="data_form.project_id"
                        filterable
                        remote
                        reserve-keyword
                        placeholder="请选择项目"
                        :remote-method="project_filter"
                        :loading="project_input.loading"
                        remote-show-suffix
                     >
                        <el-option
                            v-for="item in project_input.extra_options"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        />
                        <el-option
                            v-for="item in project_input.options"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="用例描述" prop="description">
                    <el-input v-model="data_form.description" />
                </el-form-item>
            </el-form>
        </div>
        <div style="display: flex;justify-content: end;height: 7%;align-items: center;">
            <el-button type="primary" @click="sumit_form(formRef)" style="margin-right: 20px;">保 存</el-button>
        </div>
    </div>
</template>

<script lang="ts" setup name="webCaseInput">
import { ref,reactive,onMounted } from 'vue';
import { ElMessage,FormInstance,FormRules } from 'element-plus'
import { AddCase,GetCase,EditCase,GetProjectSelect,WebCaseStepCopy } from '../api'
import { WebTestCaseType} from '../types'
import { useProjectConfig } from '/@/stores/projectConfig';
import { ProjectSelectType } from '/@/types/autotest'

//mode: 0: 新增 1:编辑 2:复制
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
// 回调函数定义
const emit = defineEmits(['onFinish']);

// 项目配置存储
const projectConfig = useProjectConfig();

const formRef = ref<FormInstance>();

// 表单验证规则类型定义
const rules = reactive<FormRules<WebTestCaseType>>({
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, message: '字符至少2个及以上', trigger: 'blur' },
  ],
  project_id: [
    { required: true, message: '请选择用例项目', trigger: 'blur' },
  ],
});

const data_form = ref<WebTestCaseType>({
    name: '',
    description: '',
    project_id: '',
    project_name: '',
});


// 添加数据api
const add_data = () => {
    AddCase(data_form.value)
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
    EditCase(id,data_form.value)
    .then((res) => {
        ElMessage({
            message: '保存成功',
            type: 'success',
        })
        
    }).catch((err) => {
        console.log(err);
    });
}


// 复制用例api
const case_copy= (copy_case_id: number) => {
    var data = {copy_case_id: copy_case_id,...data_form.value};
    WebCaseStepCopy(data)
    .then((res) => {
        ElMessage({
            message: res.msg,
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
        } else if (props.mode == 2) {
            case_copy(props.id)
        }
        else {
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
    GetCase(id).then((res) => {
        data_form.value = res;
        project_input.extra_options = [{ id: data_form.value.project_id , name: data_form.value.project_name }];
    }).catch((err) => {
        console.log(err);
    })
}

// 项目选择搜索
var project_input = reactive({
    loading: false,
    options: [] as ProjectSelectType[],
    extra_options: [] as ProjectSelectType[],
    name: '',
})

const get_project_select = (name: string) => {
    var param = {
        name: name,
        "page": 1,
        "page_size": 10
    }
    GetProjectSelect(param).then((res) => {
        project_input.options = res.results;
    })
}

// 项目搜索
const project_filter = (query: string) => {
    project_input.loading = true
    setTimeout(() => {
      project_input.loading = false
      get_project_select(query)
    }, 200)
}

onMounted(() => {
    if (props.mode == 1 || props.mode == 2) {
        get_data(props.id);
    } else {
        if (typeof projectConfig.id == 'number') {
            data_form.value.project_id = projectConfig.id;
            project_input.extra_options = [{id: projectConfig.id, name: projectConfig.name}]
        }
    }
})

</script> 