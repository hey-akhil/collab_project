import json
import os
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone as dj_timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import RegisterForm, LoginForm, ProductForm
from django.core.exceptions import PermissionDenied
from .models import GalleryImage
from .forms import GalleryImageForm
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.utils.timezone import now
import os

def home(request):
    return render(request, 'app/home.html')

def contact(request):
    return render(request,'app/contact.html')

def ourServices(request):
    return render(request,'app/what_we_offer.html')

def about(request):
    return render(request, "app/about_us.html")

def cone_order(request):
    return render(request, "app/order_checkout_main_page.html")

@login_required
def profile_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        user = request.user
        user.username = new_username
        user.email = new_email
        user.save()
        return redirect('profile')

    # ✅ Get the latest order for the current user
    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()

    return render(request, 'app/profile.html', {
        'recent_orders': [latest_order] if latest_order else []
    })

def book_appointment(request):
    success = False
    if request.method == "POST":
        try:
            Booking.objects.create(
                service=request.POST["service"],
                datetime=parse_datetime(request.POST["datetime"]),
                email=request.POST["email"],
                name=request.POST["name"],
                phone=request.POST["phone"],
                description=request.POST.get("description", "")
            )
            success = True
        except Exception as e:
            print("Booking Error:", e)  # Debugging log

    return render(request, "app/book_appointment.html", {"success": success})

def adminviewpage(req):
    context = {}
    return render(req, 'app/admin/admin.html', context)

def booking_list(request):
    bookings = Booking.objects.all().order_by('-datetime')  # latest first
    return render(request, 'app/admin/Appointment_booking_list.html', {'bookings': bookings})

def reviews_page(request):
    reviews = Review.objects.all().order_by('-date_posted')  # latest first
    return render(request, 'reviews.html', {'reviews': reviews})

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "app/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("login")

def place_order(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        contact = request.POST.get('contact')
        address_line1 = request.POST.get('add1')
        street = request.POST.get('street')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('county', 'India')
        total_price = Decimal(request.POST.get('total_price', '0'))
        shipping_charge = Decimal(request.POST.get('shipping_charge', '50'))
        final_total = Decimal(request.POST.get('final_total', '0'))

        # Save order
        order = Order.objects.create(
            user=request.user,
            fullname=fullname,
            contact=contact,
            address_line1=address_line1,
            street=street,
            city=city,
            zipcode=zipcode,
            country=country,
            total_price=total_price,
            shipping_charge=shipping_charge,
            final_total=final_total
        )

        # Save order items
        colors = request.POST.getlist('color[]')
        qtys = request.POST.getlist('qty[]')
        for color, qty in zip(colors, qtys):
            price_per_item = 100 if color == "Classic Brown" else 120 if color == "Bold Black" else 150
            line_total = Decimal(price_per_item) * Decimal(qty)
            OrderItem.objects.create(order=order, color=color, quantity=qty, line_total=line_total)

        return JsonResponse({
            "status": "success",
            "message": "Your order has been placed successfully!"
        })

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def admin_dashboard(request):
    return render(request, 'app/admin/admin_dashboard.html')

def get_price_for_color(color):
    """Return price for each mehndi color."""
    prices = {
        "Classic Brown": Decimal(100),
        "Bold Black": Decimal(120),
        "Reddish Maroon": Decimal(150),
    }
    return prices.get(color, Decimal(0))

# View to show all orders
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'app/admin/order_list.html', {'orders': orders})

# View to show single order details
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()  # fetch related OrderItems
    return render(request, 'app/admin/order_detail.html', {
        'order': order,
        'order_items': order_items
    })

from django.shortcuts import get_object_or_404, redirect

def appointment_booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'app/admin/Appointment_booking_list.html', {'bookings': bookings})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect(reverse('Appointment_booking_list'))

def gallery(request):
    gallery_data = GalleryImage.objects.all()
    return render(request, 'app/gallery.html',{'gallery_data': gallery_data} )

def our_product(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'app/product.html', {'products': products})


def manage_user(request):
    return render(request, 'app/admin/user_manage.html')

def cart(request):
    return render(request, 'app/cart.html')

@login_required
def cart_view(request):
    """Display the user's cart items and total price."""
    cart_items = CartItem.objects.filter(user=request.user)
    print(f"User: {request.user}, Cart Count: {cart_items.count()}")  # Debug log

    total_price = sum(item.subtotal for item in cart_items)

    return render(request, 'app/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart or update quantity if it already exists."""
    product = get_object_or_404(Product, id=product_id)

    # Get or create a cart item for this user and product
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        # If already in cart, just increment quantity

        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'app/admin/manage_product.html', {'products': products})


@login_required
@user_passes_test(is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'app/admin/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
@user_passes_test(is_staff)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'app/admin/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
@user_passes_test(is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('manage_products')

@login_required
def my_orders(request):
    """Display all orders of the logged-in user."""
    orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")

    return render(request, "app/my_orders.html", {
        "orders": orders,
        "user_profile": request.user,  # Optional: for user details on page
    })


@login_required
def checkout_view(request):
    # Get all cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal for item in cart_items)
    shipping_charge = 50
    final_total = total_price + shipping_charge

    # Fetch all saved addresses of the user
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'app/order_checkout_main_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_charge': shipping_charge,
        'final_total': final_total,
        'addresses': addresses,  # Pass addresses to template
    })

@login_required
def place_order(request):
    user = request.user

    # Show checkout page with cart and addresses
    if request.method == "GET":
        addresses = Address.objects.filter(user=user)
        cart_items = CartItem.objects.filter(user=user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        shipping_charge = 50 if cart_items else 0
        final_total = total_price + shipping_charge
        return render(request, "place_order.html", {
            "cart_items": cart_items,
            "total_price": total_price,
            "shipping_charge": shipping_charge,
            "final_total": final_total,
            "addresses": addresses,
        })

    # Handle placing order
    if request.method == "POST":
        selected_address_id = request.POST.get("selected_address")
        total_price = float(request.POST.get("total_price", 0))
        shipping_charge = float(request.POST.get("shipping_charge", 0))
        final_total = float(request.POST.get("final_total", 0))

        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return JsonResponse({"success": False, "message": "Your cart is empty."}, status=400)

        # Use existing address or create new one
        if selected_address_id:
            address = get_object_or_404(Address, id=selected_address_id, user=user)
        else:
            address = Address.objects.create(
                user=user,
                full_name=request.POST.get("fullname"),
                contact=request.POST.get("contact"),
                address_line1=request.POST.get("add1"),
                street=request.POST.get("street"),
                city=request.POST.get("city"),
                zipcode=request.POST.get("zipcode"),
                country=request.POST.get("county", "India")
            )

        # Create order
        order = Order.objects.create(
            user=user,
            fullname=address.full_name,
            contact=address.contact,
            address_line1=address.address_line1,
            street=address.street,
            city=address.city,
            zipcode=address.zipcode,
            country=address.country,
            total_price=total_price,
            shipping_charge=shipping_charge,
            final_total=final_total
        )

        # Add items to the order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                color=item.product.color,
                quantity=item.quantity,
                line_total=item.subtotal
            )

        # Clear the cart after order placement
        cart_items.delete()

        # Return JSON response for SweetAlert + redirect
        return JsonResponse({
            "success": True,
            "message": "Your order has been placed successfully!",
            "redirect_url": "/my-orders"
        })

    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)

@login_required
def update_cart_quantity(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        try:
            new_qty = int(request.POST.get("quantity"))
            if new_qty >= 1:
                item.quantity = new_qty
                item.save()
        except ValueError:
            pass  # handle invalid input gracefully
    return redirect('cart')

@csrf_exempt  # For AJAX CSRF; required with JS fetch()
@login_required
def update_cart_quantity_ajax(request, item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quantity = int(data.get("quantity"))
            if quantity >= 1:
                item = CartItem.objects.get(id=item_id, user=request.user)
                item.quantity = quantity
                item.save()
                return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "invalid"})

@login_required
def myOrders(request):
    user = request.user
    orders = (
        Order.objects.filter(user=user)
        .prefetch_related('orderitem_set')
        .order_by('-created_at')  # Assuming you have a created_at field
    )

    return render(request, 'app/my_orders.html', {'orders': orders})

@login_required
def manage_addresses(request, pk=None):
    address = None
    if pk:  # Editing existing address
        address = get_object_or_404(Address, id=pk, user=request.user)

    if request.method == "POST":
        if address:  # Update
            address.full_name = request.POST['full_name']
            address.contact = request.POST['contact']
            address.address_line1 = request.POST['address_line1']
            address.street = request.POST.get('street', '')
            address.city = request.POST['city']
            address.zipcode = request.POST['zipcode']
            address.country = request.POST.get('country', 'India')
            address.save()
        else:  # Create
            Address.objects.create(
                user=request.user,
                full_name=request.POST['full_name'],
                contact=request.POST['contact'],
                address_line1=request.POST['address_line1'],
                street=request.POST.get('street', ''),
                city=request.POST['city'],
                zipcode=request.POST['zipcode'],
                country=request.POST.get('country', 'India')
            )
        return redirect('manage_addresses')

    addresses = Address.objects.filter(user=request.user)
    return render(request, "app/save_address.html", {"addresses": addresses, "address": address})

@login_required
def save_address(request):
    if request.method == "POST":
        pk = request.POST.get('address_id')
        if pk:
            # Edit existing
            address = get_object_or_404(Address, id=pk, user=request.user)
            address.full_name = request.POST['full_name']
            address.contact = request.POST['contact']
            address.address_line1 = request.POST['address_line1']
            address.street = request.POST.get('street', '')
            address.city = request.POST['city']
            address.zipcode = request.POST['zipcode']
            address.country = request.POST.get('country', 'India')
            address.save()
        else:
            # Add new
            Address.objects.create(
                user=request.user,
                full_name=request.POST['full_name'],
                contact=request.POST['contact'],
                address_line1=request.POST['address_line1'],
                street=request.POST.get('street', ''),
                city=request.POST['city'],
                zipcode=request.POST['zipcode'],
                country=request.POST.get('country', 'India')
            )
        return redirect('manage_addresses')

def delete_address(request, id):
    if request.method in ["POST", "GET"]:
        try:
            address = get_object_or_404(Address, id=id, user=request.user)
            address.delete()
            messages.success(request, "✅ Address deleted successfully!")
        except PermissionDenied:
            messages.error(request, "❌ You are not allowed to delete this address.")
        except Exception as e:
            messages.error(request, f"❌ Something went wrong: {str(e)}")
    else:
        messages.error(request, "❌ Invalid request method.")

    return redirect('manage_addresses')

def userlist(request):
    # Show only active users
    users = User.objects.filter(is_active=True)
    return render(request, 'app/admin/user_manage.html', {'users': users})

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if not user:
            return JsonResponse({'status': 'fail', 'message': 'User not found.'})
        # Just deactivate instead of deleting
        print(user)
        user.is_active = False
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User deactivated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def edit_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if not user:
            # redirect
            return redirect('/users')

        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users')
        else:
            form = UserEditForm(instance=user)

        return render(request, 'app/admin/edit_user.html', {'form': form, 'user': user})


def manage_gallery(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Upload new image
        image = request.FILES['image']
        obj = GalleryImage.objects.create(image=image)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'id': obj.id,
                'new_image_url': obj.image.url,
                'uploaded_at': obj.uploaded_at.strftime("%b %d, %Y %H:%M")
            })
        return redirect('manage_gallery')

    gallery = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'app/admin/manage_gallery.html', {'gallery': gallery})

def edit_gallery_image(request, id):
    image = get_object_or_404(GalleryImage, pk=id)
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            image = form.save()
            return JsonResponse({
                'success': True,
                'id': image.pk,
                'new_image_url': image.image.url,
                'uploaded_at': image.uploaded_at.strftime('%b %d, %Y %H:%M')
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    # Non-AJAX fallback
    form = GalleryImageForm(instance=image)
    return render(request, 'gallery/edit_gallery_image.html', {'form': form})

def delete_gallery_image(request, id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            image = GalleryImage.objects.get(pk=id)
            image.delete()
            return JsonResponse({'success': True})
        except GalleryImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'})
    raise Http404()