from django.contrib import admin
from django.urls import path, include
from apis import views
from apis.routers import CourierRouter



router = CourierRouter()
router.register(r'couriers', views.CourierView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
