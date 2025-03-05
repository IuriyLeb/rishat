import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        item = self.get_object()
        return Response(
            {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY},
            template_name='item_detail.html'
            )

    @action(detail=True, methods=['get'])
    def buy(self, request, pk=None):
        item = self.get_object()
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        currency = item.currency if item else settings.DEFAULT_CURRENCY

        line_items = [{
            "price_data": {
                "currency": currency,
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        }]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=settings.SITE_URL + "/success/",
            cancel_url=settings.SITE_URL + "/cancel/"
        )

        return JsonResponse({"session_id": session.id})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        return Response(
            {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY},
            template_name='order_detail.html'
            )

    @action(detail=True, methods=['get'])
    def buy(self, request, pk=None):
        order = self.get_object()
        currency = order.items.first().currency if order.items.exists() else settings.DEFAULT_CURRENCY
        stripe.api_key = settings.STRIPE_PRIVATE_KEY

        line_items = []
        for item in order.items.all():
            line_item = {
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": item.price,
                },
                "quantity": 1,
            }

            if order.tax:
                tax_rate = stripe.TaxRate.create(
                    display_name=order.tax.name,
                    percentage=order.tax.percentage,
                    inclusive=False
                )
                line_item["tax_rates"] = [tax_rate.id]

            line_items.append(line_item)

        discounts = []
        if order.discount:
            coupon = stripe.Coupon.create(
                percent_off=order.discount.percentage,
                duration="once"
            )
            discounts.append({"coupon": coupon.id})

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            discounts=discounts,
            success_url=settings.SITE_URL + "/success/",
            cancel_url=settings.SITE_URL + "/cancel/"
        )

        return Response({"session_id": session.id})