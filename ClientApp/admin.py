from django.contrib import admin
from .models import *

# Register Booking model
admin.site.register(Booking)
# Register Review model
admin.site.register(Review)
# Register Profile model
admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Address)

# Inline for OrderItem in Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Register Order model with inline OrderItems
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "fullname", "final_total", "created_at")

# Register OrderItem separately (optional, but useful)
admin.site.register(OrderItem)
