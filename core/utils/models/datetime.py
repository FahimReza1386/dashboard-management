from django.db import models
from django.utils.translation import gettext_lazy as _

class AbstractDateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        abstract = True
        verbose_name = _("Abstract Base Model")
        verbose_name_plural = _("Abstract Base Models")
        