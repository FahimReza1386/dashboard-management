# Django Imports
import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

"""
        Creating Validation For Accounts App...     
"""


def is_valid_iranian_national_code(value):
    if not re.match(r'^(?!([0-9])\1{9})\d{10}$', value):
        raise ValidationError(_("The National Code is Not Valid.."))
    
    digits = [int(d) for d in value]
    check_digit = digits[-1]
    
    s = sum(digits[i] * (10 - i) for i in range(9))
    remainder = s % 11
    
    if remainder < 2:
        if check_digit != remainder:
            raise ValidationError(_("The National Code is Not Valid.."))
    else:
        if check_digit != 11 - remainder:
            raise ValidationError(_("The National Code is Not Valid.."))
