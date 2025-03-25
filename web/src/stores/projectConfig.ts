import { defineStore } from 'pinia';
import { ProjectSelectType } from '/@/types/autotest'


export const useProjectConfig = defineStore('projectConfig', {
	state: (): ProjectSelectType => ({
		id: '',
		name: '',
	})
    ,
    actions: {
        setProject(id: number, name: string) {
            this.id = id;
            this.name = name;
        },
        setName(name: string) {
            this.name = name;
        }
    },
});
