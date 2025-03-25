
from datetime import datetime,timedelta

from django_celery_beat.models import ClockedSchedule
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


from rest_framework import serializers
from datetime import timedelta, datetime

class AdjustedDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, data):
        # 反序列化时（存储时），减去8小时
        if isinstance(data, str):
            data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        data -= timedelta(hours=8)
        return super().to_internal_value(data)

    def to_representation(self, value):
        # 序列化时（展示时），加上8小时
        if value is not None:
            value += timedelta(hours=8)
        return super().to_representation(value)

class ClockedScheduleSerializer(ModelSerializer):
    clocked_time = AdjustedDateTimeField()
    
    class Meta:
        model = ClockedSchedule
        fields = '__all__'
    

class ClockedScheduleModelViewSet(ModelViewSet):
    """
    ClockedSchedule Clocked调度模型
    """
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
    ordering = 'id'  # 默认排序

    
