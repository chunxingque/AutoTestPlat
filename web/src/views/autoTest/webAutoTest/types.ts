
// 用例步骤类型
export interface CaseStepType {
    id?: string,
    name: string,
    step_order?: number,
    action?: string,
    find_method?: string,
    find_value?: string,
    input_value?: string,
    result?: number, 
    run_time?: string,
    run_log?: string
}


// 用例修改数据类型
export interface CaseDataPutType {
    case_name: string,
    case_id?: number,
    delete_steps?: number[],
    case_steps: CaseStepType[]
}

// 测试用例数据接口类型
export interface WebTestCaseType {
    id?: number | string,
    name?: string,
    description?: string,
    result?: number,
    tester?: string,
    project_id: string | number,
    project_name: string,
    create_time?: string,
    update_time?: string,
}


export interface ProjectSelectType {
    id?: number;
    name: string;
} 