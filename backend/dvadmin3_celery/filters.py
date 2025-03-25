import django_filters
from django_celery_beat.models import PeriodicTask


class PeriodicTaskFilter(django_filters.FilterSet):
  sort = django_filters.OrderingFilter(fields=('id'))
  # icontains：包含，且忽略大小写
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

  class Meta:
    model = PeriodicTask
    fields = ['enabled']