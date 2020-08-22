from django.db import models


class InstaUser(models.Model):
    DIDNT_CHECKED = 0
    RIGHT_EMAIL = 1
    HACKABLE = 2
    HACKED = 3
    UNHACKABLE = 4
    INVALID = 5


    STATUS_CHOICES = (
        (DIDNT_CHECKED, "Didn't checked"),
        (RIGHT_EMAIL, 'Right email'),
        (HACKABLE, 'Hackable'),
        (HACKED, 'Hacked'),
        (UNHACKABLE, 'Unhackable'),
        (INVALID, 'Invalid'),
    )

    # General
    ig_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=55)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    subscribers = models.PositiveIntegerField()
    subscriptions = models.PositiveIntegerField()
    city = models.CharField(max_length=200, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DIDNT_CHECKED)
    created_at = models.DateTimeField(auto_now_add=True)

    # Process attributes
    is_processed = models.BooleanField(default=False)
    is_scrapping = models.BooleanField(default=False)

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
    count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    class Meta:
        verbose_name = 'Scrapping process'
        verbose_name_plural = 'Scrapping processes'
        ordering = ('created_at', )


class Log(models.Model):
    task = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]
    
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ('-created_at', )
