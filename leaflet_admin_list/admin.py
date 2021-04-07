import functools
import json
import operator

from django.contrib.gis.db.models import GeometryField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .filters import BoundingBoxFilter
from .version import __version__


class LeafletAdminListMixin(object):
    #: overriding list view default template
    change_list_template = 'leaflet_admin_list/leaflet_admin_list.html'

    class Media:
        css = {'all': [
            'leaflet/leaflet.css',
            'leaflet/draw/leaflet.draw.css',
            '//cdn.jsdelivr.net/npm/leaflet-mouse-position/src/L.Control.MousePosition.css',
        ]}
        js = [
            'leaflet/leaflet.js',
            'leaflet/draw/leaflet.draw.js',
            'leaflet/leaflet.extras.js',
            'leaflet/leaflet.forms.js',
            '//cdn.jsdelivr.net/npm/leaflet-mouse-position/src/L.Control.MousePosition.js',
            '//cdnjs.cloudflare.com/ajax/libs/leaflet-plugins/3.3.1/control/Permalink.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/Colors.js/1.2.4/colors.min.js',
        ]

    def changelist_view(self, request, extra_context=None):
        '''Overriden to modify changelist view'''
        q = self.model.objects.all().none()
        try:
            cl = self.get_changelist_instance(request)
            q = cl.result_list
        except Exception:
            pass

        extra_context = {
            **(extra_context or {}),
            'geojson': json.dumps(self.get_geojson_feature_list(request, q)),
            'version': __version__,
        }
        return super().changelist_view(request, extra_context)

    def get_list_filter(self, request):
        '''Overriden to add the default Bounding Box Filter'''
        list_filter = super().get_list_filter(request)
        if not list_filter:
            list_filter = []
        for f in list_filter:
            if isinstance(f, type) and issubclass(f, BoundingBoxFilter):
                return list_filter
        # The BBFilter should always be present here
        return list_filter + [BoundingBoxFilter]

    def get_geojson_feature_list(self, request, queryset):
        '''returns the whole GeoJSON `FeatureList` instance representing a `queryset`'''
        return {
            'type': 'FeatureCollection',
            'features': functools.reduce(operator.add, (self.get_geojson_features(request, o, queryset) for o in queryset), [])
        }

    def get_geojson_features(self, request, o, queryset):
        '''returns the `features` member of the `FeatureList` instance for the model instance `o`'''
        return [
            self.get_geojson_feature(request, name, o, queryset)
            for name in self.get_geojson_geometry_fields(request, o, queryset)
        ]

    def get_geojson_geometry_fields(self, request, o, queryset):
        '''returns a list of geometry field names need to be included into the feature list'''
        geometry_fields = getattr(self, 'geometry_fields', [])
        if not geometry_fields:
            geometry_fields = [f.name for f in self.model._meta.get_fields() if isinstance(f, GeometryField)]
        return geometry_fields

    def get_geojson_feature(self, request, name, o, queryset):
        '''returns a GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        return {
            'type': 'Feature',
            'geometry': self.get_geojson_geometry(request, name, o, queryset),
            'properties': self.get_geojson_properties(request, name, o, queryset),
        }

    def get_geojson_geometry(self, request, name, o, queryset):
        '''returns a `geometry` member of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        return json.loads(getattr(o, name).geojson)

    def get_geojson_properties(self, request, name, o, queryset):
        '''returns a `properties` member of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        r = {
            'field': name,
            'app_label': o._meta.app_label,
            'model_name': o._meta.model_name,
            'pk': o.pk,
        }
        popup = self.get_geojson_feature_popup(request, name, o, queryset)
        tooltip = self.get_geojson_feature_tooltip(request, name, o, queryset)
        point_style = self.get_geojson_feature_point_style(request, name, o, queryset)
        line_style = self.get_geojson_feature_line_style(request, name, o, queryset)
        if popup:
            r['popup'] = popup
        if tooltip:
            r['tooltip'] = tooltip

        if point_style:
            r['point_style'] = point_style
        if line_style:
            r['line_style'] = line_style
        return r

    def get_geojson_feature_verbose_name(self, request, name, o, queryset):
        '''returns a verbose name of the instance `o` geometry field `name` which is used to create popup and tooltip'''
        return str(self.model._meta.get_field(name).verbose_name)

    def get_geojson_feature_popup(self, request, name, o, queryset):
        '''returns a `popup` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        return (
            '<div>'
            '<a title="%(view_edit)s" href="%(link)s">'
            '<b><i>%(instance)s</i></b>'
            '</a>'
            '</div>'
        ) % {
            'view_edit': _('View/Edit %(model_verbose_name)s') % {
                'model_verbose_name': self.model._meta.verbose_name,
            },
            'instance': '%s' % o,
            'link': reverse('admin:%s_%s_change' % (
                self.model._meta.app_label,
                self.model._meta.model_name,
            ), args=[o.pk]),
        }

    def get_geojson_feature_tooltip(self, request, name, o, queryset):
        '''returns a `tooltip` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        return (
            '%(instance)s: %(verbose_name)s'
        ) % {
            'verbose_name': self.get_geojson_feature_verbose_name(request, name, o, queryset),
            'instance': '%s' % o,
        }

    def get_geojson_feature_point_style(self, request, name, o, queryset):
        '''returns a `point_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        icon = self.get_geojson_feature_icon_style(request, name, o, queryset)
        if icon:
            return {
                'icon': icon
            }

    def get_geojson_feature_icon_style(self, request, name, o, queryset):
        '''returns an `icon` member of the `point_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        pass

    def get_geojson_feature_line_style(self, request, name, o, queryset):
        '''returns a `line_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
        return {
            'color': '#A0A0A0',
            'fillColor': '#A0A0A0',
        }
