# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask, CrontabSchedule, cronexp, IntervalSchedule,ClockedSchedule
from rest_framework import serializers
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from  dvadmin3_celery.filters import PeriodicTaskFilter

from dvadmin.utils.json_response import SuccessResponse, ErrorResponse

CrontabSchedule.__str__ = lambda self: '{0} {1} {2} {3} {4} {5}'.format(
    cronexp(self.minute), cronexp(self.hour),
    cronexp(self.day_of_month), cronexp(self.month_of_year),
    cronexp(self.day_of_week), str(self.timezone)
)

from dvadmin.utils.serializers import CustomModelSerializer

from dvadmin.utils.viewset import CustomModelViewSet

# 任务列表，给前端选择
TASK_MAP = {
     'WebAutoTest.tasks.task__start_case': '启动WebUi用例',
     'dvadmin3_celery.tasks.task__send_email': '测试',
     'dvadmin3_celery.tasks.task__send_email_param': '测试(带参数)',
}

def get_job_list():
    from application import settings
    task_list = []
    task_dict_list = []
    for app in settings.INSTALLED_APPS:
        try:
            exec(f"""
from {app} import tasks
for ele in [i for i in dir(tasks) if i.startswith('task__')]:
    task_dict = dict()
    task_dict['label'] = '{app}.tasks.' + ele
    task_dict['value'] = '{app}.tasks.' + ele
    task_list.append('{app}.tasks.' + ele)
    task_dict_list.append(task_dict)
                """)
        except ImportError:
            pass
    return {'task_list': task_list, 'task_dict_list': task_dict_list}


def get_job_list_static():
    """手动生成job列表"""
    task_dict_list = []
    for key,value  in TASK_MAP.items():
        task_dict_list.append( {'label': value, 'value': key})
    return task_dict_list

class CeleryCrontabScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = CrontabSchedule
        exclude = ('timezone',)

class AdjustedDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        # 序列化时（展示时），加上8小时
        if value is not None:
            value += timedelta(hours=8)
        return super().to_representation(value)


class PeriodicTasksSerializer(CustomModelSerializer):
    # crontab = serializers.StringRelatedField(read_only=True)
    last_run_at = AdjustedDateTimeField()

    class Meta:
        model = PeriodicTask
        fields = '__all__'


class PeriodicTasksCreateSerializer(CustomModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class CeleryTaskModelViewSet(CustomModelViewSet):
    """
    CeleryTask 添加任务调度
    """

    queryset = PeriodicTask.objects.exclude(name="celery.backend_cleanup")
    serializer_class = PeriodicTasksSerializer
    create_serializer_class = PeriodicTasksCreateSerializer
    # filter_fields = ['name','task', 'enabled']
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PeriodicTaskFilter
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            handle_data = []
            for item in serializer.data:
                item['task_type'] = TASK_MAP.get(item['task']) if  TASK_MAP.get(item['task']) else item['task']
                if item['interval']:
                    item['schedule_type'] = 0
                    interval =  IntervalSchedule.objects.filter(id=item['interval']).first()
                    item['schedule'] =interval.__str__()
                elif item['crontab']:
                    item['schedule_type'] = 1
                    crontab =  CrontabSchedule.objects.filter(id=item['crontab']).first()
                    item['schedule'] =crontab.__str__()
                elif item['clocked']:
                    item['schedule_type'] = 2
                    clocked = ClockedSchedule.objects.filter(id=item['clocked']).first()
                    date_time = clocked.clocked_time + timedelta(hours=8)
                    date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
                    item['schedule'] = date_time_str
                else:
                    item['schedule_type'] = 3
                    item['schedule'] = ''
                handle_data.append(item)
            return self.get_paginated_response(handle_data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def job_list(self, request, *args, **kwargs):
        """获取所有任务"""
        # result = get_job_list()
        # task_list = result.get('task_dict_list')
        task_list = get_job_list_static()
        return SuccessResponse(msg='获取成功', data=task_list, total=len(task_list))

    def create(self, request, *args, **kwargs):
        body_data = request.data.copy()
        schedule_type = body_data.get('schedule_type')
        schedule = body_data.get('schedule')
        task = body_data.get('task')
        kwargs = body_data.get('kwargs') if body_data.get('kwargs') else '{}'
                       
        task_list = get_job_list().get('task_list')
        data_dict = {
            'task': task, 
            'name': body_data.get('name'), 
            'kwargs': kwargs,
            'enabled': body_data.get('enabled',False),
            'one_off': body_data.get('one_off',False),
        }

        if task not in task_list:
            return ErrorResponse(msg="添加失败, 没有该任务", data=None)

        if schedule_type == 0:
            # 处理间隔调度
            interval_schedule = IntervalSchedule.objects.filter(id=schedule).first()
            if not interval_schedule:
                return ErrorResponse(msg="无效的间隔调度ID", data=None)
            data_dict['interval'] = interval_schedule
        elif schedule_type == 1:
            # 处理定时调度
            cron_schedule = CrontabSchedule.objects.filter(id=schedule).first()
            if not cron_schedule:
                return ErrorResponse(msg="无效的定时调度ID", data=None)
            data_dict['crontab'] = cron_schedule
        elif schedule_type == 2:
            clocked_schedule = ClockedSchedule.objects.filter(id=schedule).first()
            data_dict['clocked'] = clocked_schedule
            data_dict['one_off'] = True
        else:
            return ErrorResponse(msg="无效的调度类型", data=None)

        try:
            periodic_task = PeriodicTask.objects.create(**data_dict)
        except ValidationError as e:
            return ErrorResponse(msg=f"添加失败: {e.messages}", data=None)

        serializer = PeriodicTasksCreateSerializer(periodic_task)
        return SuccessResponse(msg="添加成功", data=serializer.data)
    

    def destroy(self, request, *args, **kwargs):
        """删除定时任务"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse(data=[], msg="删除成功")

    @action(detail=True, methods=['post'])
    def update_status(self, request, *args, **kwargs):
        """开始/暂停任务"""
        instance = self.get_object()
        body_data = request.data
        instance.enabled = body_data.get('enabled')
        instance.save()
        return SuccessResponse(msg="修改成功", data=None)


