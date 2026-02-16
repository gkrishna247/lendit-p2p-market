"""
Models for the LendIt P2P Marketplace.

Defines the core data structures:
- Item: An item listed for rent by a user.
- Booking: A rental booking made by a user for an item.
"""

from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    """An item listed for peer-to-peer rental."""

    class Category(models.TextChoices):
        """Available item categories for browsing and filtering."""

        ELECTRONICS = "electronics", "Electronics"
        TOOLS = "tools", "Tools"
        HOME = "home", "Home"
        OUTDOORS = "outdoors", "Outdoors"
        OTHER = "other", "Other"

    STATUS_CHOICES = [
        ("available", "Available"),
        ("rented", "Rented"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    daily_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    """A rental booking linking a renter to an item."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("returned", "Returned"),
    ]

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="bookings"
    )
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.renter.username} - {self.item.title}"
