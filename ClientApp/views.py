from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking
def home(request):
    return render(request, 'app/home.html')

def contact(request):
    return render(request,'app/contact.html')

def book_appointment(request):
    if request.method == "POST":
        Booking.objects.all.create(
            service=request.POST["service"],
            datetime=request.POST["datetime"],
            email=request.POST["email"],
            name=request.POST["name"],
            phone=request.POST["phone"],
            description=request.POST.get("description", "")
        )
        return HttpResponse("✅ Booking Successful!")
    return render(request, "app/book_appointment.html")

def adminviewpage(req):
    context = {}
    return render(req, 'app/admin/admin.html', context)

def booking_list(request):
    bookings = Booking.objects.all().order_by('-datetime')  # latest first
    return render(request, 'app/admin/Appointment_booking_list.html', {'bookings': bookings})
