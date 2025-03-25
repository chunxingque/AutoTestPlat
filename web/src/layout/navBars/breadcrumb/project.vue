<template>
    <div>
        <el-select
            v-model="project_config.id"
            filterable
            remote
            reserve-keyword
            remote-show-suffix
            placeholder="请选择项目"
            :remote-method="project_filter"
            :loading="project_data.loading"
            @change="changeSelect"
            :empty-values="[null, undefined]"
            >
            <el-option label="所有项目" value="" />
            <el-option
                v-for="item in project_data.options"
                :key="item.id"
                :label="item.name"
                :value="item.id"
            />
        </el-select>
    </div>
</template>

<script setup lang="ts" >
import { reactive } from 'vue';
import { request } from '/@/utils/service';
import { useProjectConfig } from '/@/stores/projectConfig'
import { ProjectSelectType } from '/@/types/autotest'

const project_config = useProjectConfig()

// 查询产品选择列表
function GetProjectSelect(query: any) {
    return request({
        url: "/webtestcase/projectselect/",
        method: 'get',
        params: query,
    });
}

// 项目搜索
var project_data = reactive({
    loading: false,
    options: [] as ProjectSelectType[],
})


const get_project_select = (name: string) => {
    var param = {
        name: name,
        "page": 1,
        "page_size": 10
    }
    GetProjectSelect(param).then((res) => {
        project_data.options = res.results;
    })
}

const changeSelect = (value: number) => {
    const selectedOption = project_data.options.find(option => option.id == value);
    if (selectedOption) {
        project_config.setName(selectedOption.name);
    }
};

// 项目搜索
const project_filter = (query: string) => {
    project_data.loading = true
    setTimeout(() => {
      project_data.loading = false
      get_project_select(query)
    }, 200)
}
</script>