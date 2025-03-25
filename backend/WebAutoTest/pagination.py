from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response


class customPageNumberPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"
    page_size = 10
    max_page_size = 50 # 允许客户端通过page_size_query_param查询字符串调整的每页数据量
    
    def get_paginated_response(self, data):
        return Response({
            'code': 2000,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class customLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = "limit"
    offset_query_param = "offset"
    default_limit = 10
    max_limit = 20 # 允许客户端通过page_size_query_param查询字符串调整的每页数据量