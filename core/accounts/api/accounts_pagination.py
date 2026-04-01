# Locale Imports
from utils.api.pagination import BasePagination

class AccountsPagination(BasePagination):
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)