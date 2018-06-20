from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        user = serializer.save()

    def get_serializer_class(self):
        return UserSerializer