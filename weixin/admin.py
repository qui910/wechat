from django.contrib import admin

# Register your models here.
from weixin.models import ResourceMessage


class ResourceMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'resource_code', 'resource_name', 'resource_message', 'create_time', 'create_user'
    )

    list_filter = ('resource_code','resource_name', 'create_time')

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'resource_code')

    list_per_page = 20

    search_fields = ('resource_code', 'resource_name',)

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-create_time',)

    fieldsets = (
        ('基本信息', {
            'fields': (
                ('resource_code', 'resource_name', 'resource_message'),
            )
        }),
    )

    # 权限判断
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(ResourceMessageAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user != obj.create_user:
            return False
        return True

    # 保存信息
    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.save()


admin.site.register(ResourceMessage, ResourceMessageAdmin)
admin.site.site_title = "微信公众号后台管理系统"
admin.site.site_header = "微信公众号后台管理系统"
admin.site.index_title = '资源信息管理'
