from.models import *
from rest_framework import serializers

class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ('courier_id', 'assign_time', 'complete_time', 'courier_type',)

class OrderIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("order_id",)

class OrderAssignResponse(serializers.Serializer):
    orders = OrderIdSerializer(many=True)
    # assign_time = serializers.CharField()