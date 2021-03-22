from django.db import models
from django.db.models import F, ExpressionWrapper, DurationField, Avg, Min, Count
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
    def assign_order(self, courier_id): # todo: correct order setting algoritm
        max_weight = {'foot': 10,
                      'bike': 15,
                      'car': 50}

        courier = Courier.objects.get(pk=courier_id)
        orders = Order.objects.filter(region__in=courier.regions, courier_id__isnull=True) \
                              .order_by("weight")
        if orders:
            correct_ids = select_orders_by_weight({i.order_id: i.weight for i in orders},
                                                   max_weight.get(courier.courier_type))
            sel = Order.objects.filter(pk__in=correct_ids)
            date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + "Z" # todo: adding time inconsistency???
            sel.update(courier_id=courier.courier_id,
                       assign_time=date,
                       courier_type=courier.courier_type)
            return sel, date
        else:
            return [], None

    def complete_order(self, data): # todo: починить этот позорный говнокод
        order = Order.objects.get(pk=data.get("order_id")) # todo: fix repeating
        if order:
            if data.get("courier_id") == order.courier_id:
                order.complete_time=data.get("complete_time")
                order.save(update_fields=['complete_time'])
                return True
            else:
                return False
        else:
            return False

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

    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES)
    regions = models.JSONField(default=list, blank=True, null=True) # todo: integer validation
    working_hours = models.JSONField(default=list, blank=True, null=True) # todo: string validation

    add_funcs = CourierManager()
    objects = models.Manager()


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
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, blank=True, null=True)
    assign_time = models.DateTimeField(auto_now=False, blank=True, null=True) # "yyyy-MM-ddTHH:mm:ssZ" .strftime("%Y-%m-%d%H:%M:%S")
    complete_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    courier_type = models.CharField(max_length=4, choices=COURIER_TYPE_CHOICES, blank=True, null=True) # todo: repeating choices???

    objects = models.Manager()
    test_man = OrderManager()
