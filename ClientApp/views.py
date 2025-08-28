from time import timezone

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone as dj_timezone
from .models import Booking
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from .models import Booking,Review,OrderItem,Order
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test


def home(request):
    return render(request, 'app/home.html')

def contact(request):
    return render(request,'app/contact.html')

def ourServices(request):
    return render(request,'app/what_we_offer.html')

def about(request):
    return render(request, "app/about_us.html")

def cone_order(request):
    return render(request, "app/cone_order.html")

def profile(request):
    return render(request, "app/profile.html")

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

def manage_gallery(request):
    return render(request, 'app/admin/manage_gallery.html')

def our_product(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'app/product.html', {'products': products})

def manage_product(request):
    return render(request, 'app/admin/manage_product.html')

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