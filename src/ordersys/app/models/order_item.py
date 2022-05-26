from django.db import models

from app.models import Course, Order


class OrderItem(models.Model):
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

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Avoid null=True for text fields, ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/#null
    # blank=True is necessary if we want to allow empty string,
    # ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.Field.blank
    requirements = models.TextField(default="", blank=True)
    status = models.CharField(max_length=2, choices=STATUSES, default=STATUS_RECEIVED)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'OrderItem - {self.course.name} - {self.status}'
