import django_filters
from . import models


class WebTestCaseFilter(django_filters.FilterSet):
  sort = django_filters.OrderingFilter(fields=('id'))
  # icontains：包含，且忽略大小写
  project_name = django_filters.CharFilter(field_name='project_id__name', lookup_expr='icontains')
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

  class Meta:
    model = models.WebTestCase
    fields = ['result','project_id']
    
class WebTestStepFilter(django_filters.FilterSet):
  sort = django_filters.OrderingFilter(fields=('id'))
  # icontains：包含，且忽略大小写
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

  class Meta:
    model = models.WebTestStep
    fields = ['case_id']


class ProjectSelectFilter(django_filters.FilterSet):
  sort = django_filters.OrderingFilter(fields=('id'))
  # icontains：包含，且忽略大小写
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

  class Meta:
    model = models.Project
    fields = ['id']