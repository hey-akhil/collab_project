from django.contrib import admin
from .models import Booking,Order,OrderItem,CartItem,Product,Review,Profile

admin.site.register(Booking)

admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Profile)

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "fullname", "final_total", "created_at")

admin.site.register(OrderItem)
