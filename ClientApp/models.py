from django.db import models

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
