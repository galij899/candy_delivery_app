from.models import *
from rest_framework import serializers

class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'

