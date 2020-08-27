from datetime import timedelta

from django.utils import timezone
from django.contrib import admin
from django.shortcuts import redirect
from django.db.models import Q

from core.models import InstaUser, Process, Log, Controller, APIKey, SpeedLog
from core.utils import format_date_from_seconds
from core.tasks import check_api_keys_task

from admin_actions.admin import ActionsModelAdmin


@admin.register(InstaUser)
class InstaUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'subscribers', 'city', 'formated_update_date',)
    list_filter = ('status', 'is_processed', 'is_invalid_process')
    fields = ('ig_id', 'username', 'name', 'email', 'phone', 'subscribers', 'subscriptions', 'city',
                'status', 'tid', 'api_key', 'is_processed', 'is_invalid_process', 'is_scrapping', 'created_at', 'updated_at')
    readonly_fields = ('updated_at', 'created_at')


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'formated_create_date', 'formated_update_date')
    list_display_links = ('user',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('tid', 'api_key', '__str__', 'action', 'formated_create_date')


@admin.register(Controller)
class ControllerAdmin(ActionsModelAdmin):
    list_display = ('is_finished', 'is_stopped', 'formated_update_date')
    actions_row = ('stop_parse', 'resume_parse')
    
    def stop_parse(self, request, pk):
        obj = Controller.objects.get(pk=pk)
        obj.is_stopped = True
        obj.save()
        message = "Parsing has been stopped!"
        self.message_user(request, message)
        return redirect("admin:core_controller_changelist")
    stop_parse.short_description = 'Stop parsing'
    stop_parse.url_path = 'stop-parse/'
    
    def resume_parse(self, request, pk):
        obj = Controller.objects.get(pk=pk)
        obj.is_stopped = False
        obj.save()
        message = "Parsing has been resumed!"
        self.message_user(request, message)
        return redirect("admin:core_controller_changelist")
    resume_parse.short_description = "Resume parsing"
    resume_parse.url_path = 'resume-parse/'


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('username', 'api_key', 'formated_checked_date', 'active')
    actions = ('check_api_keys',)

    def check_api_keys(self, request, queryset):
        for pk in queryset.values_list('pk', flat=True):
            check_api_keys_task.delay(pk)
    check_api_keys.short_description = 'Check API keys'


@admin.register(SpeedLog)
class SpeedLogAdmin(admin.ModelAdmin):
    list_display = ('count', 'formated_created_date')
    actions = ('clear_logs',)

    def clear_logs(self, request, queryset):
        current_datetime = timezone.now()
        last_datetime = current_datetime.replace(hour=current_datetime.hour-1)
        SpeedLog.objects.filter(~Q(created_at__range=(last_datetime, current_datetime))).delete()
        message = 'Old logs have been removed!'
        self.message_user(request, message)
        return redirect("admin:core_speedlog_changelist")
    clear_logs.short_description = "Remove old logs"


admin.site.site_header = f'Django administration ({InstaUser.get_percent_email()}' \
    f'--{InstaUser.get_percent_valid_email()}' \
    f'--{InstaUser.get_percent_hacked()})' \
    f' {SpeedLog.calculate_speed()}'
