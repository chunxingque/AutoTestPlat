import { request } from '/@/utils/service';

export const url_prefix = '/api/dvadmin_celery/clockedschedule/';

// 查询用例列表
export function GetClockedList(query: any) {
    return request({
        url: url_prefix,
        method: 'get',
        params: query,
    });
}

// 添加用例
export function AddClocked(data: any) {
    return request({
        url: url_prefix,
        method: 'post',
        data: data
    });
}

// 查询单个web用例
export function GetClocked(id: number) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'get',
    });
}

// 修改用例
export function EditClocked(id: number,data: any) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'put',
        data: data
    });
}

// 删除用例与步骤
export function DelClocked(id: number) {
    return request({
        url: `${url_prefix}${id}/`,
        method: 'delete',
    });
}
