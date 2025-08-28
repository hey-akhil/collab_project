from django.contrib import admin
from .models import Booking,Order,OrderItem

admin.site.register(Booking)

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "fullname", "final_total", "created_at")

admin.site.register(OrderItem)
