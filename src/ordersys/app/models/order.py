import datetime

from django.db import models

from app.models.table import Table


class Order(models.Model):
    STATUS_RECEIVED = 'C'
    STATUS_PREPARING = 'P'
    STATUS_READY = 'R'
    STATUS_DELIVERED = 'D'

    STATUSES = [
        (STATUS_RECEIVED, 'Received'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_READY, 'Ready'),
        (STATUS_DELIVERED, 'Delivered'),
    ]

    date = models.DateField(default=datetime.date.today)
    # unique_for_date only works for Admin site
    # ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/#unique-for-date
    # Hiding the `date` field from Admin site breaks this check
    # ref: https://django-users.narkive.com/OGaaB4PF/unique-for-date-not-working
    calling_number = models.PositiveSmallIntegerField(unique_for_date="date")
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUSES, default=STATUS_RECEIVED)

    def __str__(self):
        return f'Order[{self.calling_number}] - Table {self.table.index} - {self.status}'
