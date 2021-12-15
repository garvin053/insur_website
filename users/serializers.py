from datetime import datetime

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'nationality', 'first_name', 'last_name', 'city',
                  'emer_contact_num', 'emer_contact_person',
                  'gender',
                  'zipcode', 'street')

# 'date_joined', 'is_staff',