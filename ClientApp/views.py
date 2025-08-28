from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from .models import Booking
from .forms import RegisterForm, LoginForm
from .models import Booking,Review,OrderItem,Order
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from django.shortcuts import render, get_object_or_404

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
        fullname = request.POST.get("fullname")
        contact = request.POST.get("contact")
        add1 = request.POST.get("add1")
        street = request.POST.get("street")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("county", "India")

        colors = request.POST.getlist("color[]")
        quantities = request.POST.getlist("qty[]")

        shipping_charge = Decimal(50)
        total_price = Decimal(0)

        for i, color in enumerate(colors):
            price = get_price_for_color(color)
            qty = int(quantities[i])
            total_price += price * qty

        final_total = total_price + shipping_charge

        order = Order.objects.create(
            fullname=fullname,
            contact=contact,
            address_line1=add1,
            street=street,
            city=city,
            zipcode=zipcode,
            country=country,
            total_price=total_price,
            shipping_charge=shipping_charge,
            final_total=final_total,
        )

        for i, color in enumerate(colors):
            price = get_price_for_color(color)
            qty = int(quantities[i])
            OrderItem.objects.create(
                order=order,
                color=color,
                quantity=qty,
                line_total=price * qty
            )

        # Set success message
        messages.success(request, f"Your order (ID: {order.id}) has been placed successfully!")

        return redirect('order')  # back to the form page

    # if GET request, fallback
    return redirect('order')

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
    return render(request, 'app/admin/order_detail.html', {'order': order})