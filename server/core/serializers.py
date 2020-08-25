from rest_framework import serializers

from core.models import InstaUser, Process, Log

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaUser
        fields = ('username', 'email', 'subscribers')
        