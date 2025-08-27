from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact-us/', views.contact, name="contact"),
    path('make-my-booking/', views.book_appointment, name="booking"),
    path('admin-page/', views.adminviewpage, name="admin"),
    path('Appointment_booking_list/', views.booking_list, name="Appointment_booking_list"),
    path('make-my-booking/', views.book_appointment, name="booking"),
    path('our-services/', views.ourServices, name="our_services"),
    path("about-us/", views.about, name="about"),
    path("order/", views.cone_order, name="order"),

]