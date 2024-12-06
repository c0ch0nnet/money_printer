from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet

from api.models import Manager
from api.permissions import RequestPermission
from api.serializers import GroupSerializer, UserSerializer, ManagerSerializer

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


from django.shortcuts import render

# Create your views here.

# class Index(APIView):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


class ManagerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Manager.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        return queryset

    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated, RequestPermission]

