from __future__ import absolute_import, print_function

from leaflet.admin import LeafletGeoAdminMixin

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from leaflet_admin_list.admin import LeafletAdminListMixin
from leaflet_admin_list.filters import BoundingBoxFilter

from .models import Building, DeliveryJob, Waypoint


class WaypointAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, ModelAdmin):
    list_display = ["name", ]


admin.site.register(Waypoint, WaypointAdmin)


class DeliveryJobAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, ModelAdmin):
    list_display = ["name", "quantity", "weight", "price", "kind"]
    list_filter = ["quantity", "kind", BoundingBoxFilter]


admin.site.register(DeliveryJob, DeliveryJobAdmin)


class BuildingAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, ModelAdmin):
    list_display = ["name", ]


admin.site.register(Building, BuildingAdmin)
