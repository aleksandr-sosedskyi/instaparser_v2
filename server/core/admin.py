from datetime import timedelta

from django.core.cache import cache
from django.urls import path

from django.utils import timezone
from django.contrib import admin
from django.shortcuts import redirect
from django.db.models import Q

from core.models import InstaUser, Process, Log, Controller, APIKey, SpeedLog, UserHistory, BlackListWords, Queue
from core.tasks import check_api_keys_task
from core.filters import GoodUsersFilter

from admin_actions.admin import ActionsModelAdmin


class UserHistoryAdmin(admin.TabularInline):
    model = UserHistory
    list_display = ('__str__', 'email', 'phone', 'city')
    readonly_fields = ('__str__', 'created_at', 'email', 'phone', 'city')
    can_delete = False
    extra = 0
    

@admin.register(InstaUser)
class InstaUserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/insta_user__changelist.html'
    list_display = ('username', 'email', 'phone', 'subscribers', 'city', 'created_at', 'formated_update_date')
    list_filter = (GoodUsersFilter, 'status', 'is_processed', 'is_invalid_process', 'group')
    fields = ('ig_id', 'username', 'name', 'email', 'phone', 'subscribers', 'subscriptions', 'city',
                'status', 'tid', 'api_key', 'is_processed', 'is_invalid_process', 'is_scrapping', 'created_at', 'updated_at')
    readonly_fields = ('updated_at', 'created_at')
    inlines = [
        UserHistoryAdmin,
    ]
    search_fields = ('username', 'email', 'city')
    actions = ('set_not_interesting',)

    def set_not_interesting(self, request, queryset):
        queryset.update(status=InstaUser.NOT_INTERESTING)
        message = 'Selected users have been marked as not interesing!'
        self.message_user(request, message)
        return redirect('admin:core_instauser_changelist')
    set_not_interesting.short_description = 'Mark as not interesting'

    def get_urls(self):
        urls = [
            path('get-info/', self.get_info, name='get_info')
        ]
        return urls + super().get_urls()
    
    def get_info(self, request):
        cache.clear()
        qs = InstaUser.objects.all()
        qs_emails = qs.filter(~Q(email=None))
        qs_phones = qs.filter(~Q(phone=None))
        qs_cities = qs.filter(~Q(city=None))
        emails_count = qs_emails.count()
        right_emails_count = qs_emails.filter(status=InstaUser.RIGHT_EMAIL).count()
        phone_count = qs_phones.count()
        cities_count = qs_cities.count()
        message = f"Users: {'{:,}'.format(qs.count())}. Emails: {emails_count}. Right emails: {right_emails_count}. Phones: {phone_count}. Cities: {cities_count}"
        self.message_user(request, message)
        return redirect('admin:core_instauser_changelist')


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'count', 'formated_create_date', 'formated_update_date')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('tid', 'api_key', '__str__', 'action', 'formated_create_date')
    fields = ('message', 'tid', 'api_key', 'action', 'formated_create_date')
    readonly_fields = ('message', 'tid', 'api_key', 'action', 'formated_create_date')


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
    change_list_template = 'admin/api_key__changelist.html'
    list_display = ('username', 'api_key', 'formated_create_date', 'formated_check_date', 'active')

    def get_urls(self):
        urls = [
            path('check-api-keys/', self.check_api_keys, name='check_api_keys')
        ]
        return urls + super().get_urls()

    def check_api_keys(self, request):
        for i in APIKey.objects.all():
            check_api_keys_task.delay(i.pk)
        message = 'Task is successfully started!'
        self.message_user(request, message)
        return redirect('admin:core_apikey_changelist')


@admin.register(SpeedLog)
class SpeedLogAdmin(admin.ModelAdmin):
    list_display = ('count', 'formated_create_date')
    fields = ('count', 'formated_create_date')
    readonly_fields = ('count', 'formated_create_date')

    change_list_template = 'admin/speed_logs__changelist.html'

    def get_urls(self):
        urls = [
            path('refresh-speed-logs/', self.clear_logs, name='refresh_speed_logs')
        ]
        return urls + super().get_urls()

    def clear_logs(self, request):
        current_datetime = timezone.now()
        last_datetime = current_datetime.replace(hour=current_datetime.hour-1)
        SpeedLog.objects.filter(~Q(created_at__range=(last_datetime, current_datetime))).delete()
        message = 'Old logs have been removed!'
        self.message_user(request, message)
        return redirect("admin:core_speedlog_changelist")


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'city', 'formated_create_date')
    list_display_links = ('user',)
    readonly_fields = ('user',)


@admin.register(BlackListWords)
class BlackListWordsAdmin(admin.ModelAdmin):
    list_display = ('word',)


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('username', 'parse_friends', 'formated_create_date')

    
# Uncomment after migrate
admin.site.site_header = f'Django administration ({InstaUser.objects.get_percent_email()}' \
    f'--{InstaUser.objects.get_percent_valid_email()}' \
    f'--{InstaUser.objects.get_percent_hacked()})' \
    f' {SpeedLog.objects.calculate_speed()}.' \
    f' {Queue.objects.all().count()}'
