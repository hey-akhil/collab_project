from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    service = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.datetime}"

class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField(default=5)  # 1–5 stars
    date_posted = models.DateField(auto_now_add=True)
    customer_photo = models.ImageField(upload_to='reviews/', blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}⭐"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    fullname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="India")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.fullname}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.color} x {self.quantity}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional image field

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.color} - {self.size}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user} - {self.product.name}"