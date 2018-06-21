from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active','url',)
        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class BearerTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                msg = ('User not found.')
                raise serializers.ValidationError(msg)

            if user:
                if (check_password(password, user.password) == False):
                    msg = ('Password is incorrect.')
                    raise serializers.ValidationError(msg)
                pass
            else:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg)

        data['user'] = user
        return data


class UnauthenticatedUserSerializer(UserSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('password', 'first_name', 'is_active','url',)
        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user