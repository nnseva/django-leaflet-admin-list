import functools
import operator

from django.contrib import admin
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.geos import Polygon
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class BoundingBoxFilter(admin.SimpleListFilter):
    title = _('Bounding Box')
    parameter_name = 'bounding_box'
    template = 'leaflet_admin_list/leaflet_admin_filter.html'

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        polygon = self.get_bbox(self.value())
        fields = self.get_geometry_fields(request, queryset)
        return queryset.filter(functools.reduce(operator.or_, [Q(**{'%s__intersects' % name: polygon}) for name in fields]))

    def has_output(self):
        return True

    def bbox_selected(self):
        return self.value() or ''

    def lookups(self, request, model_admin):
        bbox = self.bbox_selected()
        return (
            (bbox, _('Current map bounding box')),
        )

    def get_geometry_fields(self, request, queryset):
        geometry_fields = getattr(self, 'geometry_fields', [])
        if not geometry_fields:
            geometry_fields = [f.name for f in queryset.model._meta.get_fields() if isinstance(f, GeometryField)]
        return geometry_fields

    def get_bbox(self, value):
        try:
            bbox = [float(c) for c in value.split(',')]
        except Exception:
            return None
        if len(bbox) != 4:
            return None
        p0, p1 = [[bbox[0], bbox[1]], [bbox[2], bbox[3]]]
        return Polygon([
            p0, [p0[0], p1[1]],
            p1, [p1[0], p0[1]],
            p0
        ])
