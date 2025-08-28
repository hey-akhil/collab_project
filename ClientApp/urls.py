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
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("order/", views.cone_order, name="order"),
    path("place-order/", views.place_order, name="place_order"),
    path("my-profile/", views.profile, name="profile"),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

]