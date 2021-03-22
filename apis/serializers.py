from.models import *
from rest_framework import serializers
from .models import Courier

class CourierSerializer(serializers.ModelSerializer): # todo: correct order of fields
    rating = serializers.SerializerMethodField()
    earnings = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = '__all__'

    def get_rating(self, obj):
        return Courier.add_funcs.rating(obj.courier_id)

    def get_earnings(self, obj):
        return Courier.add_funcs.earnings(obj.courier_id)

    def to_representation(self, instance):
        """
        Удаляет пустые поля рейтинга и заработка
        """
        rep = super(serializers.ModelSerializer, self).to_representation(instance)

        if rep.get('rating') is None:
            rep.pop('rating')

        if rep.get('earnings') is None:
            rep.pop('earnings')

        return rep


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