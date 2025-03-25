<template>
    <div style="display: flex; flex-direction: column; height: 100%;">
        <div style="height: 93%;">
            <el-form 
                ref="formRef"
                :model="webstep_form" 
                :rules="rules"
                label-width="auto" 
                label-position="top" 
                style="max-width: 100%; padding: 20px"
            >
                <el-form-item label="步骤名称" prop="name">
                    <el-input v-model="webstep_form.name" />
                </el-form-item>
                <el-form-item label="操作" prop="action">
                    <el-cascader
                        v-model="webstep_form.action"
                        :options="webAutoTestStore.action"
                        @change=""
                        :props="{ emitPath: false }"
                        style="width: 100%;"
                    />
                </el-form-item>
                <div v-if="webstep_form.action=='webpage_open'">
                    <el-form-item label="URL地址" prop="input_value" :rules="{required: true,message: '请输入URL地址'}">
                        <el-input v-model="webstep_form.input_value" placeholder="" />
                    </el-form-item>
                </div>
                <div v-else-if="webstep_form.action=='sleep'">
                    <el-form-item label="等待时间(s)" prop="input_value">
                        <el-input v-model="webstep_form.input_value" placeholder="" :rules="{required: true}" />
                    </el-form-item>
                </div>
                
                <div v-else-if="webstep_form.action=='mouse_move_click'">
                    <el-form-item label="坐标位置" prop="input_value" :rules="{required: true,message: '请输入坐标位置'}" >
                        <el-input v-model="webstep_form.input_value" placeholder="200,200" />
                    </el-form-item>
                    <el-form-item label="元素定位方法" prop="find_method" :rules="{required: false,message: '请选择元素定位方法'}">
                        <el-select v-model="webstep_form.find_method" placeholder="定位方法" >
                            <el-option
                                v-for="item in webAutoTestStore.find_method"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            /> 
                        </el-select>
                    </el-form-item>
                    <el-form-item label="元素查找值" prop="find_value" :rules="{required: false,message: '请输入元素查找值'}">
                        <el-input v-model="webstep_form.find_value"  placeholder="" />
                    </el-form-item>
                    <el-alert type="info" :closable="false">
                        <p>此操作会先计算坐标位置，最后对坐标位置进行点击。适合一些元素不好定位的场景。</p>
                        <p>请注意，设置元素和不设置元素的坐标起点会不同。</p>
                        <li>如果不设置元素，会从视窗左上角（原点）进行偏移。</li>
                        <li>如果设置元素,会将光标移动到元素中心点（原点），然后通过偏移量进行光标相对原点的偏移。</li>
                    </el-alert>
                </div>
                <div v-else-if="webstep_form.action=='mouse_scroll'">
                    <el-form-item label="鼠标滚动值" prop="input_value" :rules="{required: true,message: '请输入鼠标滚动值'}" >
                        <el-input v-model="webstep_form.input_value" placeholder="300" />
                    </el-form-item>
                    <el-form-item label="元素定位方法" prop="find_method" :rules="{required: false,message: '请选择元素定位方法'}">
                        <el-select v-model="webstep_form.find_method" placeholder="定位方法" >
                            <el-option
                                v-for="item in webAutoTestStore.find_method"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            /> 
                        </el-select>
                    </el-form-item>
                    <el-form-item label="元素查找值" prop="find_value" :rules="{required: false,message: '请输入元素查找值'}">
                        <el-input v-model="webstep_form.find_value"  placeholder="" />
                    </el-form-item>
                    <el-alert type="info" :closable="false">
                        <p>鼠标滚动，鼠标滚动值为正值向下滚动,为负值向上滚动。</p>
                        <p>滚动到指定元素，需要设置元素，它会先滚动到指定元素，然后继续滚动鼠标滚动值，如果只想滚动指定的元素，请把鼠标滚动值设置为0</p>
                    </el-alert>
                </div>
                <div v-else-if="webstep_form.action.includes('click') || webstep_form.action=='hover'">
                    <el-form-item label="元素定位方法" prop="find_method" :rules="{required: true,message: '请选择元素定位方法'}">
                    <el-select v-model="webstep_form.find_method" placeholder="定位方法" >
                    <el-option
                        v-for="item in webAutoTestStore.find_method"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    /> 
                    </el-select>
                    </el-form-item>
                    <el-form-item label="元素查找值" prop="find_value" :rules="{required: true,message: '请输入元素查找值'}">
                        <el-input v-model="webstep_form.find_value"  placeholder="" />
                    </el-form-item>
                </div>
                <div v-else-if="webstep_form.action=='text_input'">
                    <el-form-item label="元素定位方法" prop="find_method" :rules="{required: true,message: '请选择元素定位方法'}">
                    <el-select v-model="webstep_form.find_method" placeholder="定位方法" >
                        <el-option
                            v-for="item in webAutoTestStore.find_method"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        /> 
                    </el-select>
                    </el-form-item>
                    <el-form-item label="元素查找值" prop="find_value" :rules="{required: true,message: '请输入元素查找值'}">
                        <el-input v-model="webstep_form.find_value"  placeholder="" />
                    </el-form-item>
                    <el-form-item label="文本输入值" prop="input_value" :rules="{required: true,message: '请输入文本'}" >
                        <el-input v-model="webstep_form.input_value" placeholder="" />
                    </el-form-item>
                </div>
                <div v-else-if="webstep_form.action=='keyboard_input'">
                    <el-form-item label="键盘按键" prop="input_value" :rules="{required: true,message: '请选择URL按键'}">
                        <el-select
                                v-model="webstep_form.input_value"
                                filterable
                                remote
                                reserve-keyword
                                placeholder="请选择按键"
                                :remote-method="keyboard_input_filter"
                                :loading="keyboard_input.loading"
                            >
                                <el-option
                                v-for="item in keyboard_input.options"
                                :key="item"
                                :label="item"
                                :value="item"
                                />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="元素定位方法" prop="find_method">
                    <el-select v-model="webstep_form.find_method" placeholder="定位方法" >
                    <el-option
                        v-for="item in webAutoTestStore.find_method"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    /> 
                    </el-select>
                    </el-form-item>
                    <el-form-item label="元素查找值" prop="find_value">
                        <el-input v-model="webstep_form.find_value"  placeholder="" />
                    </el-form-item>
                    
                </div>
                <div v-if="webstep_form.action=='webpage_window'">
                    <el-form-item label="选择跳转窗口" prop="input_value" :rules="{required: true,message: '请选择跳转窗口'}">
                        <el-select
                                v-model="webstep_form.input_value"
                                placeholder="选择跳转窗口"
                            >
                                <el-option
                                v-for="item in webAutoTestStore.webpage_window"
                                :key="item"
                                :label="item.label"
                                :value="item.value"
                                />
                        </el-select>
                    </el-form-item>
                    <el-alert type="info" :closable="false">
                        <p>窗口标签页操作</p>
                        <p>注意: 当点击链接跳转到一个新窗口时,驱动获取的还是旧窗口的元素,获取不到新窗口的元素，需要添加一个步骤,切换到新窗口,一般最后一个窗口就是新窗口。</p>
                    </el-alert>
                </div>
                
            </el-form>
        </div>
        <div style="display: flex;justify-content: end;height: 7%; border-top-style: solid;border-top-width: thin; align-items: center;">
            <el-button type="primary" @click="sumit_form(formRef)" style="margin-right: 20px;">保 存</el-button>
        </div>
    </div>
</template>

<script lang="ts" setup name="CaseStepInput">
import { ref,reactive,onMounted } from 'vue';
import { ElMessage,FormInstance,FormRules } from 'element-plus'
import { AddWebStep,GetWebStep,EditWebStep } from '../api'
import { CaseStepType } from '../types'
import { useWebAutoTest } from "/@/stores/webAutoTest"

const webAutoTestStore = useWebAutoTest();

const emit = defineEmits(['onFinish']);
// 0: 新增 1：修改 2：复制
const props = defineProps({
    case_id: {
        type: Number,
        default: 0,
    },
    step_order: {
        type: Number,
        default: 0,
    },
    step_id: {
        type: String,
        default: "",
    },
    mode: {
        type: Number,
        default: 0,
    }
});



const formRef = ref<FormInstance>();

// 表单验证规则类型定义
const rules = reactive<FormRules<CaseStepType>>({
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, message: '字符至少2个及以上', trigger: 'blur' },
  ],
  action: [
    { required: true, message: '请选择操作', trigger: 'change' },
  ],
});

const webstep_form = ref({
  case_id: props.case_id,
  step_order: 1,
  name: '',
  action: '',
  find_method: '',
  find_value: '',
  input_value: ''
});



// 添加步骤api
const add_webstep = () => {
    AddWebStep(webstep_form.value)
    .then((res) => {
        ElMessage({
            message: '保存成功',
            type: 'success',
        })
    }).catch((err) => {
        console.log(err);
    });
}

// 修改步骤api
const edit_webstep = (id: string) => {
    EditWebStep(id,webstep_form.value)
    .then((res) => {
        ElMessage({
            message: '保存成功',
            type: 'success',
        })
        
    }).catch((err) => {
        console.log(err);
    });
}


const sumit_form = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
        if (props.mode == 1) {
            edit_webstep(props.step_id as string)
        }  else {
            add_webstep()
        }
        emit('onFinish');
    } else {
      console.log('error submit!', fields)
    }
  })
}

// 获取步骤详情
const  get_web_step =  (id: string) => {
    GetWebStep(id).then((res) => {
        webstep_form.value = res.result;
    }).catch((err) => {
        console.log(err);
    })
}

onMounted(() => {
    if (props.mode==1) {
        get_web_step(props.step_id);
    }
    else if (props.mode == 2) {
        get_web_step(props.step_id);
        webstep_form.value.step_order = props.step_order;
    }
    else {
        webstep_form.value.step_order = props.step_order;
    }
})

// 按键输入框搜索
var keyboard_input = reactive({
    loading: false,
    options: [] as string[],

})

const keyboard_input_filter = (query: string) => {
  if (query) {
    keyboard_input.loading = true
    setTimeout(() => {
      keyboard_input.loading = false
      keyboard_input.options = webAutoTestStore.keyboard.filter((item) => {
        return item.toLowerCase().includes(query.toLowerCase())
      })
    }, 200)
  } else {
    keyboard_input.options = webAutoTestStore.keyboard.slice(0,5)
  }
}

</script> 