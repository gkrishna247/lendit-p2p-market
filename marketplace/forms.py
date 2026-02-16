"""
Forms for the LendIt P2P Marketplace.

Handles user registration, item creation/editing, and booking requests.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item


class UserRegisterForm(UserCreationForm):
    """Extended registration form with email field."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-input"
            field.widget.attrs["placeholder"] = field.label


class ItemForm(forms.ModelForm):
    """Form for creating and editing rental items."""

    class Meta:
        model = Item
        fields = ("title", "description", "category", "daily_price")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Canon EOS R5 Camera",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Describe your item, its condition, and any rental terms...",
                "rows": 5,
            }),
            "daily_price": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "0.00",
                "min": "0.01",
                "step": "0.01",
            }),
            "category": forms.Select(attrs={
                "class": "form-input",
            }),
        }


class BookingForm(forms.Form):
    """Form for requesting a booking on an item."""

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-input",
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-input",
        })
    )

    def clean(self):
        """Validate that end_date is after start_date."""
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if end <= start:
                raise forms.ValidationError(
                    "End date must be after start date."
                )
        return cleaned_data
