# Third-Party Imports
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "result": data,
            "count": self.page.paginator.count,
            "link":{
                "here" : self.request.build_absolute_uri(),
                "next" : self.get_next_link(),
                "previous" : self.get_previous_link(),
            },
        })
    page_size = 5