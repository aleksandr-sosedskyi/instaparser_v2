from django.db import models


class InstaUser(models.Model):
    DIDNT_CHECKED = 0
    RIGHT_EMAIL = 1
    HACKABLE = 2
    HACKED = 3
    UNHACKABLE = 4

    STATUS_CHOICES = (
        (DIDNT_CHECKED, "Didn't checked"),
        (RIGHT_EMAIL, 'Right email'),
        (HACKABLE, 'Hackable'),
        (HACKED, 'Hacked'),
        (UNHACKABLE, 'Unhackable'),
    )

    # General
    ig_id = models.CharField(primary_key=True, max_length=50)
    username = models.CharField(max_length=55)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    subscribers = models.PositiveIntegerField(null=True)
    subscriptions = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=200, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DIDNT_CHECKED)
    created_at = models.DateTimeField(auto_now_add=True)

    # Process attributes
    is_processed = models.BooleanField(default=False)
    is_scrapping = models.BooleanField(default=False)
    is_invalid_process = models.BooleanField(default=False)

    @staticmethod
    def get_users_to_parse():
        return InstaUser.objects.filter(
            is_processed=False,
            is_scrapping=False,
            is_invalid_process=False
        )

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
        return f"({self.count}){self.user.username} - {self.created_at}"

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

    task = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
    
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ('-created_at', )
