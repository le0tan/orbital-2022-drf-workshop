from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, decorators, response
from rest_framework import viewsets, permissions

from app.models import Order
from app.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permissions = [permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'table']
    ordering_fields = ['date']

    @decorators.action(detail=True, methods=['get'])
    def deliver_order(self, request, pk=None):
        order = self.get_object()
        order.status = Order.STATUS_DELIVERED
        order.save()
        return response.Response({
            'status': 'ok',
            'order': OrderSerializer(order).data
        })

    @decorators.action(detail=False, methods=['get'])
    def deliver_all_orders(self, request):
        for order in Order.objects.all():
            order.status = Order.STATUS_DELIVERED
            order.save()
        return response.Response({
            'status': 'ok'
        })
