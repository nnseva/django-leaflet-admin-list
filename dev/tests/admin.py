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

    def get_geojson_feature_line_style(self, request, name, o, queryset):
        return {
            'color': '#00F000',
            'fillColor': '#00A000',
            'fillOpacity': 1.0,
        }

    def get_geojson_feature_icon_style(self, request, name, o, queryset):
        return {
            'iconUrl': (
                'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIj8+PH'
                'N2ZyBpZD0iTGF5ZXJfMV8xXyIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW'
                '5kOm5ldyAwIDAgMTYgMTY7IiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9Ij'
                'AgMCAxNiAxNiIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dH'
                'A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cD'
                'ovL3d3dy53My5vcmcvMTk5OS94bGluayI+PHBhdGggZD0iTTgsMEMzLj'
                'U4MiwwLDAsMy41ODIsMCw4czMuNTgyLDgsOCw4czgtMy41ODIsOC04Uz'
                'EyLjQxOCwwLDgsMHogTTgsMTEuMjA3TDIuNjQ2LDUuODU0bDAuNzA3LT'
                'AuNzA3TDgsOS43OTNsNC42NDYtNC42NDYgIGwwLjcwNywwLjcwN0w4LD'
                'ExLjIwN3oiLz48L3N2Zz4='
            ),
            'iconSize': [5, 5],
            'iconAnchor': [3, 3]
        }


admin.site.register(Building, BuildingAdmin)
