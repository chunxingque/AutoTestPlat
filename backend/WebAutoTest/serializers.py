
from rest_framework import serializers
from dvadmin.utils.serializers import CustomModelSerializer
from . import models

class WebTestCaseModelSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project_id.name',required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = models.WebTestCase
        read_only_fields = ("id","create_time", )
        fields = "__all__"

class WebTestStepModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebTestStep
        fields = "__all__"

class ProjectCustomModelSerializer(CustomModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = ["id"]

class ProjectModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
 
        
class RunCaseSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()
    browser = serializers.CharField(default='chrome',allow_blank=True)
    incognito = serializers.BooleanField(default=False,allow_null=True)
    headless = serializers.BooleanField(default=False, allow_null=True)
    window_size = serializers.CharField(default='max',allow_blank=True)
    grid_url = serializers.CharField(default=None,allow_blank=True)
    run_step = serializers.IntegerField(default=0)


    