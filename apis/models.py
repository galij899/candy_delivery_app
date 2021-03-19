from django.db import models

# Create your models here.

class Courier(models.Model):
    COURIER_TYPE_CHOICES = (
        ("foot", "foot"),
        ("bike", "bike"),
        ("car", "car"),
    )

    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES)
    regions = models.JSONField()
    working_hours = models.JSONField()
    rating = models.FloatField(null=True)
    earnings = models.IntegerField()


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    courier_id = models.ForeignKey(Courier.courier_id)


class OrderItem(models.Model):
    item_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey(Order.order_id, on_delete=models.CASCADE)
    weight = models.FloatField()
    region = models.IntegerField()
    delivery_hours = models.JSONField()

