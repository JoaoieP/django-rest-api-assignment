from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BearerTokenSerializer
from .serializers import UnauthenticatedUserSerializer
from .serializers import UserSerializer


from rest_framework.decorators import detail_route
from django.contrib.auth.hashers import check_password

class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        user = serializer.save()

    @detail_route(methods=['patch'])
    def update(self, request, pk):
        user = get_user_model().objects.get(id=pk)
        if (self.request.META['HTTP_TOKEN']):
            try:
                    if (str((Token.objects.get(key=self.request.META['HTTP_TOKEN'])).user.pk) != str(pk)):
                            return Response({"detail": "Token not valid"})
            except Token.DoesNotExist:
                return Response({"detail": "Token not valid"})
            if (check_password(request.data.get("password"),user.password)):
                user.set_password(request.data.get("new_password"))
                user.save()
                return Response({"detail": "Password changed succesfully."})
            else:
                return Response({"detail": "Invalid username/password."})
        else:
            pass
            #activation goes here

    def get_serializer_class(self):
        try:
            Token.objects.get(key=self.request.META['HTTP_TOKEN'])
            return UserSerializer
        except Token.DoesNotExist:
                return UnauthenticatedUserSerializer
            


class BearerAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = BearerTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })