# Django Imports
from abc import abstractmethod

# Third-Party Imports
from rest_framework import pagination
from rest_framework.response import Response

class BasePagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 20
    
    @abstractmethod
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )