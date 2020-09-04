from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from core.models import InstaUser, Process, Log
from core.serializers import ListUsersSerializer


class ListUsersPaginator(PageNumberPagination):
    page_size = 10

    
class ListUsers(APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def get(self, request, format=None):
        user_status = request.GET.get('status')
        qs = InstaUser.objects.filter(status=user_status)
        data = ListUsersSerializer(qs, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request, format=None):
        data = request.data 
        pk = data['pk']
        status = data['status']
        try:
            user = InstaUser.objects.get(pk=pk)
        except InstaUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User does not exist'})
        user.status = status 
        user.save()
        return Response(status=status.HTTP_200_OK, data={'pk': user.pk})
