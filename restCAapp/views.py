from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BearerTokenSerializer
from .serializers import UnauthenticatedUserSerializer
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        token=Token.objects.get(user=user)
        send_mail(
                'Activation token',
                'token = {}'.format(token),
                'activate@codingassignment.so',
                [user.email],
                fail_silently=False,
            )

    @detail_route(methods=['patch'])
    def update(self, request, pk):
        """Updates account. When head has a token it looks for password, and new password in body of request. Password is changed if the given password is correct.
        If no token is present in the head it looks for a token in the body to activate account"""
        user = get_user_model().objects.get(id=pk)
        try: 
            if (self.request.META['HTTP_TOKEN']):
                try:
                    token=Token.objects.get(key=self.request.META['HTTP_TOKEN'])
                    if (str(token.user.pk) != str(pk)):
                        return Response({"detail": "Token not valid"})
                    if (check_password(request.data.get("password"),user.password)):
                        user.set_password(request.data.get("new_password"))
                        user.save()
                        return Response({"detail": "Password changed succesfully."})
                    else:
                        return Response({"detail": "Password incorrect."})
                except Token.DoesNotExist:
                    return Response({"detail": "Token not valid"})
        except KeyError:
            try:
                print(request.data.get("token"))
                token=Token.objects.get(key=request.data.get("token"))
                print(token)
                if (str(token.user.pk) != str(pk)):
                    return Response({"detail": "Token not valid"})
                else:
                    user.is_active = True
                    user.save()
                    serializer = UserSerializer(user,context={'request': request})
                    return Response(serializer.data)
            except Token.DoesNotExist:
                    return Response({"detail": "Token not valid"})


    def get_serializer_class(self):
        """Hides email and last name if no valid auth token is in the head of GET requests"""
        try:
            Token.objects.get(key=self.request.META['HTTP_TOKEN'])
            return UserSerializer
        except Token.DoesNotExist:
                return UnauthenticatedUserSerializer
        except KeyError:
            if(self.request.META['REQUEST_METHOD'] == 'POST'):
                return UserSerializer
            else:
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