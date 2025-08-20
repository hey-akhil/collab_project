from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

def home(request):
    return render(request, 'app/home.html')

def contact(request):
    return render(request,'app/contact.html')

def ourServices(request):
    return render(request,'app/what_we_offer.html')

def about(request):
    return render(request, "app/about_us.html")


def book_appointment(request):
    if request.method == "POST":
        Booking.objects.create(
            service=request.POST["service"],
            datetime=request.POST["datetime"],
            email=request.POST["email"],
            name=request.POST["name"],
            phone=request.POST["phone"],
            description=request.POST.get("description", "")
        )
        return HttpResponse("✅ Booking Successful!")
    return render(request, "app/book_appointment.html")

def reviews_page(request):
    reviews = Review.objects.all().order_by('-date_posted')  # latest first
    return render(request, 'reviews.html', {'reviews': reviews})