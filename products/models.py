from django.db import models
from uuid import uuid4
from django.utils.text import slugify

from users.models import User
from categories.models import Category
from shops.models import Shop
class Product(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4, editable=False)
    name = models.CharField(max_length=255, default="")
    thumbnails = models.TextField()
    price = models.FloatField(default=0)
    quantity_sold = models.IntegerField(default=0)
    attribute = models.JSONField()
    description = models.TextField(default="")
    slug = models.SlugField(unique=True, default="", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class Variation(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4)
    fields = models.JSONField()
    thumbnail = models.TextField()
    price = models.FloatField(default=0)
    remain_quantity = models.IntegerField(default=0)
    retail_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    origin_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class Feedback(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4) 
    star = models.IntegerField(default=5)
    like = models.IntegerField(default=0)
    attachment = models.TextField(default="")
    message = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="feedbacks")
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)


STATUS_CHOICES = [(0, 'Pending'),(1, 'Shipping'),(2, 'Delivered'),(3, 'Cancel'),]
class Order(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('order', 'variation',)



