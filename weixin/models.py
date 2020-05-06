from django.db import models
import django.utils.timezone as timezone
# Create your models here.


class ResourceMessage(models.Model):
    resource_name = models.CharField(max_length=100, verbose_name="资源名称", null=False)
    resource_message = models.CharField(max_length=250, verbose_name="资源信息", null=False)
    resource_code = models.IntegerField(unique=True, default=10000, verbose_name='资源编码')
    create_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')
    create_user = models.CharField(max_length=100, default='admin', verbose_name='创建人')

    def __str__(self):
        return '<ResourceMessage:{}>'.format(self.resource_name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    class Meta:
        verbose_name_plural = verbose_name = '资源信息'
