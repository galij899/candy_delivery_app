from .models import Courier, Order, OrderManager
from rest_framework.response import Response
from rest_framework import viewsets, views, permissions
from .serializers import CourierSerializer, OrderSerializer, OrderIdSerializer, CourierPostSerializer
from rest_framework import status
from rest_framework.decorators import action
import datetime
import json

# Create your views here.

def success_post(data, basename):
    return {f"{basename}s": [{"id": data[item].get(f"{basename}_id")} for item in range(len(data))]}

class CourierView(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierPostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        return {'couriers': [{'id': instance.get('courier_id')} for instance in serializer.save().get("data")]}

    def create(self, request, *args, **kwargs):
        serializer = CourierPostSerializer(data=request.data, context={"i": 1})
        if not serializer.is_valid(raise_exception=False): # todo: create same validation for all requests
            validation_errors = {"validation_error": serializer.errors["data"]}
            return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs): # todo: add as a mixin
        serializer = self.get_serializer(data=request.data["data"], many=isinstance(request.data["data"], list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(success_post(serializer.data, "order"), status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"]) # todo: transform and put in manager
    def assign(self, request):
        obj, date = Order.test_man.assign_order(request.data.get("courier_id"))
        if obj:
            serializer = OrderIdSerializer(obj, many=True)
            return Response(json.dumps({"orders": serializer.data, "assign_time": date}))
        else:
            return Response(json.dumps({"orders": []}))

    @action(detail=True, methods=["post"])
    def complete(self, request):
        result = Order.test_man.complete_order(request.data)
        # print(result)
        if result: # todo: use serializer
            return Response(json.dumps({"order_id": request.data.get("order_id")}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) # todo: 400 empty body?
