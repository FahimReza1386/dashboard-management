# Django Imports
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler to provide consistent error responses.
    """
    
    response = exception_handler(exc, context)
    
    if response is not None:
        status_code = response.status_code
        if status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                "status": "error",
                "message": _("Authentication credentials were not provided or are invalid."),
                "detail":str(exc),
            }
        elif status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                "status": "error",
                "message": _("You do not have permission to perform this action."),
                "detail": str(exc),
            }
        elif status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                "status": "error",
                "message": _("The requested resource was not found."),
                "detail":str(exc),
            }
        elif status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                "status": "error",
                "message": _("Bad request. Please check your input data."),
                "detail":str(exc),
            }
        elif status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            response.data = {
                "status": "error",
                "message": _("An internal server error occurred. Please try again later."),
                "detail":str(exc),
            }
            
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict) or isinstance(exc.detail, list):
                response.data["detail"] = exc.detail
            elif isinstance(exc.detail, str):
                response.data["detail"] = exc.detail
            else:
                if hasattr(exc, 'get_full_details'):
                    response.data["detail"] = exc.get_full_details()
                else:
                    response.data["detail"] = str(exc.detail)

        response.data = response.data

    return Response(response.data, status=status_code)
