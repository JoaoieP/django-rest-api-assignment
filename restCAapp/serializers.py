from django.contrib.auth import get_user_model
from rest_framework.serializers import HyperlinkedModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active','url')
        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        return user