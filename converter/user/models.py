from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    title = models.CharField(max_length=400, verbose_name="title", db_index=True)
    description = models.TextField(default="", verbose_name="description")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="crated at")
    file = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    user = models.ForeignKey(User, null=True, default=None, verbose_name="User",
                             related_name="user", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        return self.title

