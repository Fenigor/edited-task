from django.db import models


class webResources(models.Model):
    link: models.CharField = models.TextField(
        verbose_name='link', blank=False, null=False,
    )
    image_reference: models.TextField = models.TextField(
        verbose_name='string to the image in the file system',
        blank=False,
        null=False
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
