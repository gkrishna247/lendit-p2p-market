"""URL patterns for the marketplace app."""

from django.urls import path

from . import views

urlpatterns = [
    # Public
    path("", views.home, name="home"),
    path("items/", views.item_list, name="item-list"),
    path("items/<int:pk>/", views.item_detail, name="item-detail"),
    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Item management
    path("items/new/", views.item_create, name="item-create"),
    # Bookings
    path("items/<int:pk>/book/", views.booking_create, name="booking-create"),
    path("my-bookings/", views.my_bookings, name="my-bookings"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Booking actions
    path(
        "bookings/<int:pk>/<str:action>/",
        views.booking_action,
        name="booking-action",
    ),
]
