from django.db import models


class Project(models.Model):
    id = models.BigAutoField(primary_key=True,db_comment="项目id")
    name = models.CharField(max_length=255,db_comment="项目名称")
    description = models.TextField(blank=True, null=True,db_comment="项目描述")
    
    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'project'

class WebTestCase(models.Model):
    """web自动化测试用例表"""
    id = models.BigAutoField(primary_key=True,db_comment="用例id")
    name = models.CharField(max_length=255, blank=True, null=True,db_comment="用例名称")
    description = models.TextField(blank=True, null=True,db_comment="用例描述")
    result = models.IntegerField(default=0,blank=True, null=True,db_comment="用例结果,0未执行,1成功,2失败")
    tester = models.CharField(max_length=255, blank=True, null=True,db_comment="测试用户")
    # project_id = models.BigAutoField(blank=True, null=True,db_comment="项目id")
    project_id = models.ForeignKey(to=Project,to_field="id",on_delete=models.DO_NOTHING,db_column="project_id",related_name='webtestcase', blank=True, null=True,db_comment="项目id")
    run_time = models.DateTimeField(blank=True, null=True,db_comment="用例执行时间")
    create_time = models.DateTimeField(auto_now_add=True,db_comment="创建时间")

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'webtestcase'

class WebTestStep(models.Model):
    """web自动化测试步骤表"""
    id = models.CharField(primary_key=True,max_length=255,db_comment="步骤id")
    case_id = models.BigIntegerField(db_comment="用例id")
    step_order = models.IntegerField(blank=True, null=True,db_comment="步骤顺序")
    name = models.CharField(max_length=255, blank=True, null=True,db_comment="步骤名称")
    action = models.CharField(max_length=255, blank=True, null=True,db_comment="步骤动作")
    find_method = models.CharField(max_length=255, blank=True, null=True,db_comment="查找方法")
    find_value = models.CharField(max_length=255, blank=True, null=True,db_comment="查找值")
    input_value = models.CharField(max_length=255, blank=True, null=True,db_comment="输入值")
    result = models.IntegerField(default=0,blank=True, null=True,db_comment="步骤结果,0未执行,1成功,2失败")
    run_time = models.DateTimeField(blank=True, null=True,db_comment="步骤执行时间")
    run_log = models.CharField(max_length=255, blank=True, null=True,db_comment="运行日志")

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'webteststep'




