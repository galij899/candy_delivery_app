from .models import Courier, Order, OrderManager
from rest_framework.response import Response
from rest_framework import viewsets, views, permissions
from .serializers import CourierSerializer, OrderSerializer, OrderIdSerializer
from rest_framework import status
from rest_framework.decorators import action
import datetime
import json

# Create your views here.

def success_post(data, basename):
    return {f"{basename}s": [{"id": data[item].get(f"{basename}_id")} for item in range(len(data))]}

class CourierView(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data["data"], many=isinstance(request.data["data"], list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(success_post(serializer.data, "courier"), status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs): # todo: create logic for earnings and rating
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
        
        return Response()