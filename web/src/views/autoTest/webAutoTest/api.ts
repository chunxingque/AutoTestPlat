import { request } from '/@/utils/service';


// 查询用例列表
export function GetCaseList(query: any) {
    return request({
        url: "/webtestcase/case/",
        method: 'get',
        params: query,
    });
}

// 添加用例
export function AddCase(data: any) {
    return request({
        url: "/webtestcase/case/",
        method: 'post',
        data: data
    });
}

// 查询单个web用例
export function GetCase(id: number) {
    return request({
        url: `/webtestcase/case/${id}/`,
        method: 'get',
    });
}

// 修改用例
export function EditCase(id: number,data: any) {
    return request({
        url: `/webtestcase/case/${id}/`,
        method: 'put',
        data: data
    });
}


// 删除用例与步骤
export function DelCaseStep(id: number) {
    return request({
        url: `/webtestcase/casestep/${id}/`,
        method: 'delete',
    });
}


// 查询用例的所有步骤
export function GetWebStepList(case_id: number) {
    return request({
        url: `/webtestcase/webstep/`,
        method: 'get',
        params: {case_id},
    });
}

// web用例添加步骤
export function AddWebStep(data: any) {
    return request({
        url: "/webtestcase/webstep/",
        method: 'post',
        data: data
    });
}

// 获取步骤详情
export function GetWebStep(id: any) {
    return request({
        url: `/webtestcase/webstep/${id}/`,
        method: 'get',
    });
}

// 修改步骤
export function EditWebStep(id: string,data: any) {
    return request({
        url: `/webtestcase/webstep/${id}/`,
        method: 'put',
        data: data
    });
}

// 删除用例
export function DelWebStep(id: string) {
    return request({
        url: `/webtestcase/webstep/${id}/`,
        method: 'delete',
    });
}

// 步骤顺序移动
export function WebStepOrder(data: any) {
    return request({
        url: "/webtestcase/webstepordersort/",
        method: 'post',
        data: data
    });
}

// 用例运行
export function runCaseTask(data: any) {
    return request({
        url: "/webtestcase/runcase/",
        method: 'post',
        data: data
    });
}


// 查询产品选择列表
export function GetProjectSelect(query: any) {
    return request({
        url: "/webtestcase/projectselect/",
        method: 'get',
        params: query,
    });
}


// 步骤顺序移动
export function WebCaseStepCopy(data: any) {
    return request({
        url: "/webtestcase/webcasestepcopy/",
        method: 'post',
        data: data
    });
}