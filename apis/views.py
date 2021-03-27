from .models import Courier, Order, OrderManager
from rest_framework.response import Response
from rest_framework import viewsets, views, permissions
from .serializers import CourierSerializer, OrderSerializer, OrderIdSerializer, CourierPostSerializer, OrderPostSerializer
from rest_framework import status
from rest_framework.decorators import action
import json
from .validators.schemes import CouriersPostValidator


# Create your views here.

def success_post(data, basename):
    return {f"{basename}s": [{"id": data[item].get(f"{basename}_id")} for item in range(len(data))]}

class CourierView(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):

        if not set(request.data.keys()).issubset(set(["courier_type", "regions", "working_hours"])):
            return Response(status = status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        return {'couriers': [{'id': instance.get('courier_id')} for instance in serializer.save().get("data")]}

    def create(self, request, *args, **kwargs):
        problems = []
        for item in request.data["data"]:
            if not set([f.name for f in Courier._meta.get_fields()][1:]) == set(item.keys()):
                problems.append({"id": int(item["courier_id"])})
                request.data["data"].remove(item)
        serializer = CourierPostSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            problems += [item for item in serializer.errors["data"] if item]
        problems = [{"id": int(item.get("id"))} for item in problems]
        if problems:
            return Response(data={"validation_error": {"couriers": problems}},
                            status=status.HTTP_400_BAD_REQUEST)
        result = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=result,
                        status=status.HTTP_201_CREATED,
                        headers=headers)



class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    # def create(self, request, *args, **kwargs): # todo: add as a mixin
    #     serializer = self.get_serializer(data=request.data["data"], many=isinstance(request.data["data"], list))
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(success_post(serializer.data, "order"), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return {'orders': [{'id': instance.get('order_id')} for instance in serializer.save().get("data")]}

    def create(self, request, *args, **kwargs):
        problems = []
        for item in request.data["data"]:
            if not set([f for f in ["order_id", "weight", "region", "delivery_hours"]]) == set(item.keys()):
                problems.append({"id": int(item["order_id"])})
                request.data["data"].remove(item)
        serializer = OrderPostSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            problems += [item for item in serializer.errors["data"] if item]
        problems = [{"id": int(item.get("id"))} for item in problems]
        if problems:
            return Response(data={"validation_error": {"orders": problems}},
                            status=status.HTTP_400_BAD_REQUEST)
        result = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=result,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=True, methods=["post"])
    def assign(self, request):
        result = Order.test_man.assign_order(request.data.get("courier_id"))
        if result is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(result, list):
            return Response(data={"orders": []})
        else:
            orders, time = result
            serializer = OrderIdSerializer(orders, many=True)
            headers = self.get_success_headers(serializer.data)
            return Response(data={"orders": serializer.data, "assign_time": time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + "Z"},
                            headers=headers)

    @action(detail=True, methods=["post"])
    def complete(self, request):
        completed = Order.test_man.complete_order(request.data)
        if completed:
            return Response(data={"order_id": completed.order_id})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
