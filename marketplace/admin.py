"""Admin configuration for the LendIt marketplace."""

from django.contrib import admin

from .models import Booking, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin view for Item model."""

    list_display = ("title", "owner", "daily_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "owner__username")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin view for Booking model."""

    list_display = (
        "item",
        "renter",
        "start_date",
        "end_date",
        "total_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("item__title", "renter__username")
