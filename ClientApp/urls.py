from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact-us/', views.contact, name="contact"),
    path('make-my-booking/', views.book_appointment, name="booking")
]