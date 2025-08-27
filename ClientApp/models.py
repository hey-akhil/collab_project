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


