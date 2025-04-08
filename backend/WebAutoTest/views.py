import random
import time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


from . import models
from . import serializers
from . import filters
from .pagination import customPageNumberPagination
from dvadmin.utils.viewset import CustomModelViewSet
from .tasks import task__start_case_selenium,task__start_case_pw


class WebTestCaseModelViewSet(ModelViewSet):
    """查看所有"""
    queryset = models.WebTestCase.objects.all()
    serializer_class = serializers.WebTestCaseModelSerializer
    pagination_class = customPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filters.WebTestCaseFilter


class ProjectModelViewSet(CustomModelViewSet):
    """项目管理api
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectCustomModelSerializer

class ProjectSelectGenericAPIView(GenericAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectModelSerializer
    pagination_class = customPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filters.ProjectSelectFilter

    def get(self, request):
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page_queryset = self.paginate_queryset(queryset=queryset)
        if page_queryset is not None:
            data_ser = self.get_serializer(instance=page_queryset, many=True)
            return self.get_paginated_response(data_ser.data)
        data_ser = self.get_serializer(instance=page_queryset, many=True)
        return Response(data_ser.data)

    
            
class WebTestCaseStepInfoAPIView(APIView):
    """用例与步骤操作"""
    
    def get(self,request,case_id):
        """获取用例与步骤"""
        case_quryset = models.WebTestCase.objects.filter(id=case_id).first()
        if case_quryset is None:
            return Response({},status=status.HTTP_400_BAD_REQUEST)

        case_serializer = serializers.WebTestCaseModelSerializer(instance=case_quryset)
        
        step_queryset = models.WebTestStep.objects.filter(case_id=case_id).order_by('step_order').all()
        step_serializer = serializers.WebTestStepModelSerializer(instance=step_queryset,many=True)
        
        case_data = {
            "code": 2000, 
            "case_id": case_id,
            "case_name": case_serializer.data["name"],
            "case_steps": step_serializer.data,
        }
        
        return Response(case_data)
    
    def put(self,request,case_id):
        """修改用例与步骤"""
        req_data = request.data
        # 需要删除的步骤id数组
        delete_steps = req_data.get('delete_steps',[])
        
        case_quryset = models.WebTestCase.objects.filter(id=case_id).first()
        if case_quryset is None:
            return Response({'code': 4000,'msg': '用例不存在'},status=status.HTTP_400_BAD_REQUEST)
        
        case_data = {
            "id": case_id,
            "name": req_data.get('case_name'),
        }
        case_serializer = serializers.WebTestCaseModelSerializer(instance=case_quryset,data = case_data)
        case_serializer.is_valid(raise_exception=True)
        case_serializer.save()
        
        for item in req_data.get('case_steps'):
            if item.get('id'):
                step_queryset = models.WebTestStep.objects.filter(id=item.get('id')).first()
                if step_queryset:
                    step_serializer = serializers.WebTestStepModelSerializer(instance=step_queryset,data = item)
                    step_serializer.is_valid(raise_exception=True)
                    step_serializer.save()
            else:
                item['id'] = str(int(time.time()*1000)) + str(random.randint(1001,9999))
                item['case_id'] = case_id
                add_step_serializer = serializers.WebTestStepModelSerializer(data=item)
                add_step_serializer.is_valid(raise_exception=True)
                add_step_serializer.save()
                print(add_step_serializer.data)
        
        for item in delete_steps:
            models.WebTestStep.objects.filter(id=item).first().delete()
        
        return Response({"code": 2000, 'msg': '用例修改成功'}, status=201)
        
    
    def delete(self,request,case_id):
        """删除用例与步骤"""
        case_quryset = models.WebTestCase.objects.filter(id=case_id).first()
        if case_quryset is None:
            return Response({'code': 4000,'msg': '用例不存在'},status=status.HTTP_400_BAD_REQUEST)
        else:
            case_quryset.delete()
        
        case_steps_quryset = models.WebTestStep.objects.filter(case_id=case_id).all()
        for item in case_steps_quryset:
            item.delete()
        
        return Response({"code": 2000, 'msg': '用例删除成功'}, status=201)
    

class WebTestStepGenericViewSet(GenericViewSet):
    queryset = models.WebTestStep.objects.all()
    serializer_class = serializers.WebTestStepModelSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filters.WebTestStepFilter
    
    def list(self,request):
        case_id = request.query_params.get('case_id')
        result_data = {'code': 2000,'results': []}
        if case_id:
            queryset = models.WebTestStep.objects.filter(case_id=case_id).all().order_by('step_order')
            data_ser = self.get_serializer(instance=queryset, many=True)
            result_data['results'] = data_ser.data
            
        return Response(data=result_data,status=status.HTTP_200_OK)
    
    def create(self,request):
        request_data = request.data
        request_data['id'] = str(int(time.time()*1000)) + str(random.randint(1001,9999))
        case_id = request_data.get('case_id')
        step_order = request_data.get('step_order')
        
        serializer_ins = serializers.WebTestStepModelSerializer(data = request_data)
        serializer_ins.is_valid(raise_exception=True)
        behind_querysets = models.WebTestStep.objects.filter(case_id=case_id,step_order__gte=step_order).all().order_by('step_order')
        if behind_querysets:
            for item in behind_querysets:
                step_order = step_order + 1
                item.step_order = step_order
                item.save()
        
        serializer_ins.save()
        return Response({'code': 2000,'msg': '创建成功'},status=status.HTTP_201_CREATED)
    
    def get_pk(self,request,pk):
        # 查询数据库数据
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance=instance)
        return Response(data={'code': 2000,'result': serializer.data},status=status.HTTP_200_OK)
    
    def update(self,request,pk):
        # 查询数据库数据
        instance = self.get_object()
        # 序列化与反序列化
        serializer = self.get_serializer(instance=instance,data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        # 保存数据
        serializer.save()
        
        return Response(data=serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        """删除一个数据"""
        del_queryset = models.WebTestStep.objects.get(id=pk)
        case_id = del_queryset.case_id
        del_order = del_queryset.step_order
        del_queryset.delete()
        case_steps_quryset = models.WebTestStep.objects.filter(case_id=case_id,step_order__gt=del_order).all().order_by('step_order')
        if case_steps_quryset:
            if del_order > 0:
                start_order = del_order - 1
            else:
                start_order = 0
                
            for step_quryset in case_steps_quryset:
                start_order =  start_order + 1
                step_quryset.step_order = start_order
                step_quryset.save()
                
        return Response(status=status.HTTP_204_NO_CONTENT)


class WebStepOrderSort(APIView):
    """调整步骤顺序"""
    
    def post(self,request):
        case_id = request.data.get("case_id")
        old_order = request.data.get("old_order") 
        new_order  = request.data.get("new_order")
        if old_order == new_order:
            return Response({'code': 2000,'msg': '新旧顺序一致，无需调整'},status=status.HTTP_200_OK)
        elif abs(old_order - new_order) == 1:
            one_quryset = models.WebTestStep.objects.filter(case_id=case_id,step_order=old_order).first()
            two_quryset = models.WebTestStep.objects.filter(case_id=case_id,step_order=new_order).first()
            one_quryset.step_order = new_order
            two_quryset.step_order = old_order
            one_quryset.save()
            two_quryset.save()
            return Response({"code": 2000,"msg":"步骤顺序调整成功"},status=status.HTTP_200_OK)
        elif old_order < new_order:
            old_quryset = models.WebTestStep.objects.filter(case_id=case_id,step_order=old_order).first()
            region_qurysets = models.WebTestStep.objects.filter(case_id=case_id,step_order__gt=old_order,step_order__lte=new_order).all()
            for item in region_qurysets:
                item.step_order = item.step_order - 1
                item.save()
                
            old_quryset.step_order = new_order
            old_quryset.save()
            return Response({"code": 2000,"msg": f"步骤顺序调整成功"},status=status.HTTP_200_OK)
        elif old_order > new_order:
            old_quryset = models.WebTestStep.objects.filter(case_id=case_id,step_order=old_order).first()
            region_qurysets = models.WebTestStep.objects.filter(case_id=case_id,step_order__gte=new_order,step_order__lt=old_order).all()
            
            for item in region_qurysets:
                item.step_order = item.step_order + 1
                item.save()
                
            old_quryset.step_order = new_order
            old_quryset.save()
            return Response({"code": 2000,"msg": f"步骤顺序调整成功"},status=status.HTTP_200_OK)    
        else:
            return Response({'code': 4000,'msg': '请传入old_order和new_order两个参数'},status=status.HTTP_400_BAD_REQUEST)


class WebCaseStepCopy(APIView):
    """复制用例与步骤"""
    
    def post(self,request):
        request_data = request.data
        copy_case_id = request_data.get('copy_case_id')
        
        create_case_ser =  serializers.WebTestCaseModelSerializer(data=request_data)
        create_case_ser.is_valid(raise_exception=True)
        create_case_ser.save()
        
        step_querysets = models.WebTestStep.objects.filter(case_id=copy_case_id).all()
        if not step_querysets:
            return Response({'code': 2000,'msg': '用例没有步骤'},status=status.HTTP_200_OK)
        
        copy_step_ser = serializers.WebTestStepModelSerializer(instance=step_querysets,many=True)
        for item in copy_step_ser.data:
            item['id'] = str(int(time.time()*1000)) + str(random.randint(1001,9999))
            item['case_id'] = create_case_ser.data['id']
            add_step_serializer = serializers.WebTestStepModelSerializer(data=item)
            add_step_serializer.is_valid(raise_exception=True)
            add_step_serializer.save()
            
        return Response({"code": 2000, 'msg': '用例以及步骤复制成功'}, status=201)
        


class RunCaseTask(APIView):
    """运行用例任务"""
    
    def post(self,request):
        case_serializer = serializers.RunCaseSerializer(data=request.data)
        case_serializer.is_valid(raise_exception=True)
        auto_tool = request.data.get('auto_tool')
        if auto_tool == 'playwright':
            res = task__start_case_pw.delay(**case_serializer.data)
        else:
            res = task__start_case_selenium.delay(**case_serializer.data)
        return Response({"code": 2000,"msg":"任务已提交"},status=status.HTTP_200_OK)
         

        
        
        
        
        


        
        
        
        
        
        
        
        


