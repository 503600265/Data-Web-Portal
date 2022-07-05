from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.
from .models import *

admin.site.register(Convert)
admin.site.register(OCR)
admin.site.register(Job)
admin.site.register(Activity)

# @admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            print(ct.app_label)
            print(ct.model)
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
            # link = "<a href=\"/admin/%s/%s/%s\">%s</a>" % (ct.app_label, ct.model, obj.object_id,  link)
        return mark_safe(link)
        # http://127.0.0.1:8000/admin/tools/convert/45/change/
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
admin.site.register(LogEntry, LogEntryAdmin)
