from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from core.models import InstaUser, Process, Log
from core.serializers import ListUsersSerializer


class ListUsers(APIView):
    def get(self, request, format=None):
        user_status = request.GET.get('status')
        qs = InstaUser.objects.filter(status=user_status)
        data = ListUsersSerializer(qs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request, format=None):
        data = request.data 
        pk = data['pk']
        action = data['action']
        try:
            user = InstaUser.objects.get(pk=pk)
        except InstaUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User does not exist'})
        user.status = action 
        user.save()
        return Response(status=status.HTTP_200_OK)
