from django.db import models
from django.db.models import Q, Sum
from django.views.decorators.cache import never_cache

from django.utils import timezone

from core.utils import format_date_from_seconds


class InstaUser(models.Model):
    RIGHT_EMAIL = 1
    HACKABLE = 2
    HACKED = 3
    UNHACKABLE = 4

    STATUS_CHOICES = (
        (RIGHT_EMAIL, 'Right email'),
        (HACKABLE, 'Hackable'),
        (HACKED, 'Hacked'),
        (UNHACKABLE, 'Unhackable'),
    )

    # General
    ig_id = models.CharField(primary_key=True, max_length=50)
    username = models.CharField(max_length=55)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    subscribers = models.PositiveIntegerField(null=True)
    subscriptions = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=255, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tid = models.CharField(max_length=20)
    api_key = models.CharField(max_length=55)
    
    # Process attributes
    is_processed = models.BooleanField(default=False)
    is_scrapping = models.BooleanField(default=False)
    is_invalid_process = models.BooleanField(default=False)

    def get_users_to_parse(self):
        return self.__class__.objects.filter(
            is_processed=False,
            is_scrapping=False,
            is_invalid_process=False
        )

    def get_percent_email(self):
        all_users = self.__class__.objects.all().count()
        email_users = self.__class__.objects.filter(~Q(email=None)).count()
        return round(email_users / all_users * 100, 3)

    def get_percent_valid_email(self):
        all_users = self.__class__.objects.all().count()
        valid_email_users = self.__class__.objects.filter(status=self.__class__.RIGHT_EMAIL).count()
        return round(valid_email_users / all_users * 100, 3)

    def get_percent_hacked(self):
        all_users = self.__class__.objects.all().count()
        hacked_users = self.__class__.objects.filter(status=self.__class__.HACKED).count()
        return round(hacked_users / all_users * 100, 3)

    def formated_created_date(self):
        total_seconds = round((timezone.now() - self.created_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    def formated_update_date(self):
        total_seconds = round((timezone.now() - self.updated_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Instagram user'
        verbose_name_plural = 'Instagram users'
        ordering = ('created_at', )


class Process(models.Model):
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    tid = models.PositiveIntegerField()
    api_key = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.count})"

    def formated_update_date(self):
        total_seconds = round((timezone.now() - self.updated_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    def formated_create_date(self):
        total_seconds = round((timezone.now() - self.created_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    class Meta:
        verbose_name = 'Scrapping process'
        verbose_name_plural = 'Scrapping processes'
        ordering = ('created_at', )


class Log(models.Model):
    CHECK_API = 1
    CREATE_TASK = 2
    CREATE_USERS = 3

    ACTION_CHOICES = (
        (CHECK_API, 'Checking API'),
        (CREATE_TASK, 'Creating task'),
        (CREATE_USERS, 'Creating users')
    )

    tid = models.IntegerField(null=True)
    api_key = models.CharField(max_length=100)
    message = models.TextField()
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

    def formated_create_date(self):
        total_seconds = round((timezone.now() - self.created_at).total_seconds())
        return format_date_from_seconds(total_seconds)    

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ('-created_at', )


class Controller(models.Model):
    is_finished = models.BooleanField(default=True)
    is_stopped = models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Finished - {self.is_finished}; Stopped - {self.is_stopped}"
    
    def formated_update_date(self):
        total_seconds = round((timezone.now() - self.updated_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    class Meta:
        verbose_name = "Controller"
        verbose_name_plural = "Controllers"


class APIKey(models.Model):
    username = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} | {self.api_key}"

    def formated_checked_date(self):
        total_seconds = round((timezone.now() - self.checked_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class SpeedLog(models.Model):
    count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.count "

    def formated_created_date(self):
        total_seconds = round((timezone.now() - self.created_at).total_seconds())
        return format_date_from_seconds(total_seconds)

    def calculate_speed(self):
        current_datetime = timezone.now()
        last_datetime = current_datetime.replace(hour=current_datetime.hour-1)
        total_count = self.__class__.objects.filter(created_at__range=(last_datetime, current_datetime)).aggregate(Sum('count')).get('count__sum')
        return f"{total_count} per hour"

    class Meta:
        verbose_name = 'Speed Log'
        verbose_name_plural = 'Speed Logs'
        ordering = ('-created_at',)
