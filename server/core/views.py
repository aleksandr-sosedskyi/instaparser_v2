from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import InstaUser, Process, Log
from core.serializers import ListUsersSerializer


class ListUsers(APIView):
    def get(self, request, format=None):
        user_status = request.GET.get('status')
        qs = InstaUser.objects.filter(status=user_status)
        data = ListUsersSerializer(qs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)