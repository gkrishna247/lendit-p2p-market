"""
Root URL configuration for LendIt P2P Marketplace.

Routes all marketplace URLs through the marketplace app.
Admin site is available at /admin/.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("marketplace.urls")),
]
