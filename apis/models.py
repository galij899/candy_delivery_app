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
    regions = models.JSONField(default=list, blank=True, null=True) # todo: integer validation
    working_hours = models.JSONField(default=list, blank=True, null=True) # todo: string validation


class Order(models.Model):
    COURIER_TYPE_CHOICES = (
        ("foot", "foot"),
        ("bike", "bike"),
        ("car", "car"),
    )

    order_id = models.IntegerField(primary_key=True)
    weight = models.FloatField() # todo: validate 0.01 <= x <= 50
    region = models.IntegerField()
    delivery_hours = models.JSONField(default=list, blank=True, null=True)  # todo: string validation
    courier_id = models.ForeignKey(Courier, on_delete=models.CASCADE)
    assign_time = models.DateTimeField(auto_now=False, null=True) # "yyyy-MM-ddTHH:mm:ssZ" .strftime("%Y-%m-%d%H:%M:%S")
    complete_time = models.DateTimeField(auto_now=False, null=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES, null=True) # todo: repeating choices???