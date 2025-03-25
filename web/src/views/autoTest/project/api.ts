import { request } from '/@/utils/service';

const url_prefix='/webtestcase/project/'


// 查询用例列表
export function GetProjectList(query: any) {
    return request({
        url: url_prefix,
        method: 'get',
        params: query,
    });
}

// 添加用例
export function AddProject(data: any) {
    return request({
        url: url_prefix,
        method: 'post',
        data: data
    });
}

// 查询单个web用例
export function GetProject(id: number) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'get',
    });
}

// 修改用例
export function EditProject(id: number,data: any) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'put',
        data: data
    });
}

// 删除用例与步骤
export function DelProject(id: number) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'delete',
    });
}
