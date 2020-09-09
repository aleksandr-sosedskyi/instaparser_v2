from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from core.models import InstaUser, Process, Log
from core.serializers import ListUsersSerializer


class RightEmailUsersView(APIView):
    def get(self, request, format=None):
        qs = InstaUser.objects.filter(status=InstaUser.RIGHT_EMAIL)
        data = ListUsersSerializer(qs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, format=None):
        data = request.data
        pk = data.get('pk')
        new_status = data.get('status')
        try:
            user = InstaUser.objects.get(pk=pk)
        except InstaUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User does not exist'})
        user.status = new_status 
        user.save()
        return Response(status=status.HTTP_200_OK, data={'pk': user.pk})


class HackableUsersView(APIView):
    def get(self, request, format=None):
        qs = InstaUser.objects.filter(status=InstaUser.HACKABLE)
        data = ListUsersSerializer(qs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
