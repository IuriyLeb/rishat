from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR')
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.FloatField() # в процентах

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
    

class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.FloatField() # в процентах

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
    

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= total * (self.discount.percentage / 100)
        if self.tax:
            total += total * (self.tax.percentage / 100)
        return int(total)