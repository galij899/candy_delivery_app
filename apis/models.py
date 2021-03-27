from django.db import models
from django.db.models import F, ExpressionWrapper, DurationField, Avg, Min, Count
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


def select_orders_by_weight(d, max_weight): # todo: prettify this function
    ids = sorted(d, key=d.get)
    s = 0
    ls = []
    for id_ in ids:
        if s + d.get(id_) < max_weight:
            s += d.get(id_)
            ls.append(id_)
        else:
            break
    return ls #s, ls, [d.get(i) for i in ls]

class OrderManager(models.Manager):

    def check_batches(self, **kwargs): # todo: fix it
        try:
            go = Batch.objects.get(**kwargs)
        except Batch.DoesNotExist:
            go = None
        return go

    def assign_order(self, courier_id): # todo: correct order setting algoritm
        max_weight = {'foot': 10,
                      'bike': 15,
                      'car': 50}

        try:
            courier = Courier.objects.get(pk=courier_id)
        except:
            return None
        batch = self.check_batches(courier_id=courier.courier_id, is_complete=False)
        if batch:
            orders = Order.objects.filter(batch_id=batch.batch_id, complete_time__isnull=True)
            return orders, batch.assign_time
        else:
            try:
                orders = Order.objects.filter(region__in=courier.regions, courier_id__isnull=True) \
                                    .order_by("weight")
            except:
                return []
            correct_ids = select_orders_by_weight({i.order_id: i.weight for i in orders},
                                                   max_weight.get(courier.courier_type))
            good = Order.objects.filter(pk__in=correct_ids)
            batch = Batch.objects.create(courier_id=courier.courier_id,
                                         courier_type=courier.courier_type)
            good.update(batch_id=batch.batch_id)
            return good, batch.assign_time

    def complete_order(self, data):
        try:
            order = Order.objects.select_related().get(pk=data.get("order_id"), batch__courier_id=data.get("courier_id"))
        except:
            return None
        order.complete_time = data.get("complete_time")
        order.save(update_fields=['complete_time'])
        if not Order.objects.filter(batch_id=order.batch.batch_id, complete_time__isnull=True):
            order.batch.is_complete = True
            order.batch.save(update_fields=['is_complete'])
        return order

class CourierManager(models.Manager):
    def rating(self, courier_id):
        try:
            t = Order.objects\
                     .filter(courier_id=courier_id)\
                     .annotate(diff=ExpressionWrapper(F('complete_time')-F('assign_time'), output_field=DurationField()))\
                     .values('region')\
                     .annotate(Avg('diff'))\
                     .aggregate(Min('diff__avg'))
            real_t = round(t["diff__avg__min"].total_seconds()) # todo: prettify orm query
            rating = (60 * 60 - min(real_t, 60 * 60)) / (60 * 60) * 5
            return rating
        except:
            return None

    def earnings(self, courier_id):
        coefs = {'foot': 2,
                 'bike': 5,
                 'car': 9}

        earn = Order.objects\
                    .filter(courier_id=courier_id, complete_time__isnull=False)\
                    .values('courier_type')\
                    .annotate(Count('order_id'))
        earnings = sum(500 * [item.get('order_id__count') * coefs.get(item.get('courier_type')) for item in earn]) # todo: make more effective calculations

        return earnings if earnings != 0 else None

class Courier(models.Model):
    COURIER_TYPE_CHOICES = (
        ("foot", "foot"),
        ("bike", "bike"),
        ("car", "car"),
    )

    courier_id = models.PositiveIntegerField(primary_key=True, blank=False)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES, blank=False)
    regions = models.JSONField(blank=False)
    working_hours = models.JSONField(blank=False)

    add_funcs = CourierManager()
    objects = models.Manager()

class Batch(models.Model):
    COURIER_TYPE_CHOICES = (
        ("foot", "foot"),
        ("bike", "bike"),
        ("car", "car"),
    )
    batch_id = models.AutoField(primary_key=True)
    assign_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # "yyyy-MM-ddTHH:mm:ssZ" .strftime("%Y-%m-%d%H:%M:%S")
    is_complete = models.BooleanField(default=False)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, blank=True, null=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES, blank=True, null=True)

class Order(models.Model):
    order_id = models.PositiveIntegerField(primary_key=True, blank=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(50)], blank=False) # todo: fix 0.01 validation
    region = models.PositiveIntegerField(blank=False)
    delivery_hours = models.JSONField(blank=False)
    complete_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, blank=True, null=True) # todo: on delete

    objects = models.Manager()
    test_man = OrderManager()
