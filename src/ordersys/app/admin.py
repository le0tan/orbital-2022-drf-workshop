from django.contrib import admin

from app.models import Course, Table, Order, OrderItem

# Register your models here.
admin.site.register(Course)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
