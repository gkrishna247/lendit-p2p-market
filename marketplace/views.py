"""
Views for the LendIt P2P Marketplace.

All views are function-based for simplicity and readability.
Handles authentication, item CRUD, dashboard, and booking management.
"""

from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, ItemForm, UserRegisterForm
from .models import Booking, Item


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------


def home(request):
    """Display the homepage with all available items."""
    items = Item.objects.filter(status="available")
    return render(request, "home.html", {"items": items})


# ---------------------------------------------------------------------------
# Authentication views
# ---------------------------------------------------------------------------


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully! Please log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "marketplace/register.html", {"form": form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "marketplace/login.html")


def logout_view(request):
    """Log the user out and redirect to home."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# ---------------------------------------------------------------------------
# Item views
# ---------------------------------------------------------------------------


def item_list(request):
    """Display all available items (browse page)."""
    items = Item.objects.filter(status="available")
    return render(request, "marketplace/item_list.html", {"items": items})


def item_detail(request, pk):
    """Display a single item with booking form if applicable."""
    item = get_object_or_404(Item, pk=pk)
    booking_form = None

    # Show booking form only to logged-in users who don't own the item
    if request.user.is_authenticated and request.user != item.owner:
        booking_form = BookingForm()

    return render(
        request,
        "marketplace/item_detail.html",
        {"item": item, "booking_form": booking_form},
    )


@login_required
def item_create(request):
    """Allow authenticated users to list a new item for rent."""
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, "Item listed successfully!")
            return redirect("item-detail", pk=item.pk)
    else:
        form = ItemForm()

    return render(request, "marketplace/item_form.html", {"form": form})


# ---------------------------------------------------------------------------
# Dashboard views
# ---------------------------------------------------------------------------


@login_required
def dashboard(request):
    """Show the user's listed items and bookings received on those items."""
    my_items = Item.objects.filter(owner=request.user)
    received_bookings = Booking.objects.filter(item__owner=request.user)

    return render(
        request,
        "marketplace/dashboard.html",
        {
            "my_items": my_items,
            "received_bookings": received_bookings,
        },
    )


@login_required
def my_bookings(request):
    """Show all bookings made by the current user."""
    bookings = Booking.objects.filter(renter=request.user)
    return render(
        request,
        "marketplace/my_bookings.html",
        {"bookings": bookings},
    )


# ---------------------------------------------------------------------------
# Booking views
# ---------------------------------------------------------------------------


@login_required
def booking_create(request, pk):
    """Create a booking for an item."""
    item = get_object_or_404(Item, pk=pk)

    # Prevent booking own items
    if request.user == item.owner:
        messages.error(request, "You cannot book your own item.")
        return redirect("item-detail", pk=pk)

    if item.status != "available":
        messages.error(request, "This item is not available for booking.")
        return redirect("item-detail", pk=pk)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data["start_date"]
            end = form.cleaned_data["end_date"]

            # Validate dates are in the future
            if start < date.today():
                messages.error(request, "Start date must be today or later.")
                return redirect("item-detail", pk=pk)

            # Calculate total price
            num_days = (end - start).days
            total_price = item.daily_price * num_days

            Booking.objects.create(
                item=item,
                renter=request.user,
                start_date=start,
                end_date=end,
                total_price=total_price,
            )
            messages.success(
                request,
                f"Booking request sent! Total: ${total_price:.2f} for {num_days} day(s).",
            )
            return redirect("my-bookings")
    else:
        form = BookingForm()

    return render(
        request,
        "marketplace/item_detail.html",
        {"item": item, "booking_form": form},
    )


@login_required
def booking_action(request, pk, action):
    """Allow item owner to approve or reject a booking."""
    booking = get_object_or_404(Booking, pk=pk)

    # Only item owner can manage bookings
    if request.user != booking.item.owner:
        messages.error(request, "You are not authorized to manage this booking.")
        return redirect("dashboard")

    if booking.status != "pending":
        messages.warning(request, "This booking has already been processed.")
        return redirect("dashboard")

    if action == "approve":
        booking.status = "approved"
        booking.item.status = "rented"
        booking.item.save()
        booking.save()
        messages.success(
            request,
            f"Booking for '{booking.item.title}' approved!",
        )
    elif action == "reject":
        booking.status = "rejected"
        booking.save()
        messages.info(
            request,
            f"Booking for '{booking.item.title}' rejected.",
        )
    else:
        messages.error(request, "Invalid action.")

    return redirect("dashboard")
