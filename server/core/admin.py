from django.contrib import admin
from django.shortcuts import redirect

from core.models import InstaUser, Process, Log, Controller, APIKey

from admin_actions.admin import ActionsModelAdmin


@admin.register(InstaUser)
class InstaUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'subscribers')
    list_filter = ('status', 'is_processed')


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'created_at', 'updated_at')
    list_display_links = ('user',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('tid', '__str__', 'action', 'created_at')


@admin.register(Controller)
class ControllerAdmin(ActionsModelAdmin):
    list_display = ('is_finished', 'is_stopped')
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
    list_display = ('username', 'api_key')
