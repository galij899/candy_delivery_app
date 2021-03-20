from .models import Courier
from rest_framework.response import Response
from rest_framework import viewsets, views, permissions
from .serializers import CourierSerializer
from rest_framework import status

# Create your views here.

class CourierView(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



