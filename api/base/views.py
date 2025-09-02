from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import authentication, permissions

class TaskViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]
    
    permission_classes = [permissions.IsAuthenticated]