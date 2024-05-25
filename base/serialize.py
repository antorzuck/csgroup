from rest_framework import serializers
from .models import Referral


class ReferSl(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


