[![Tests](https://github.com/nnseva/django-leaflet-admin-list/actions/workflows/test.yml/badge.svg)](https://github.com/nnseva/django-leaflet-admin-list/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/nnseva/django-leaflet-admin-list/branch/master/graph/badge.svg?token=PT13IGSDNM)](https://codecov.io/gh/nnseva/django-leaflet-admin-list)

# Django Leaflet Admin List

![Screen Example](https://github.com/nnseva/django-leaflet-admin-list/raw/master/screen_example.png)

The [Django Leaflet Admin List](https://github.com/nnseva/django-leaflet-admin-list) package provides an admin list view
featured by the map and bounding box filter for the geo-based data of the GeoDjango. It requires
a [django-leaflet](https://github.com/makinacorpus/django-leaflet) package.

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-leaflet-admin-list
```

*Last development version* from the GitHub source version control system
```
pip install git+git://github.com/nnseva/django-leaflet-admin-list.git
```

### Compatibility notice for libgdal

Use proper versions of **libgdal** library with older Django versions.

Some strange effect of reverting coordinates in the GeoJSON (not concerning to the package, but regarding to the Django itself)
has been found with the modern **libgdal** version (2.9) and the following Django versions: *2.0, 2.1, 2.2, 3.0*

Downgrade libgdal to the **libgdal26** (present in the Ubuntu apt repository) if you would like to use such Django versions.

## Configuration

Include the `leaflet_admin_list` application into the `INSTALLED_APPS` list, like:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'leaflet',
    'leaflet_admin_list',
    ...
]
```

## Using

In your admin.py:
```python
...
from leaflet.admin import LeafletGeoAdminMixin
from leaflet_admin_list.admin import LeafletAdminListMixin
...

class WaypointAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, ModelAdmin):
    ...
```

## Visual View

Open the admin list view and see the map above the list of objects. Every object in the list is represented on the map.

Also, the bounding box filter is added to the list of filters.

Use a bounding box filter to filter objects by the geometry. Just press the 'Current map bounding box' link to filter out
objects outside of the current map bounding box. The current filtering box will be represented on the map as a rectangle. The color
of the rectangle is shown to the right of the 'Current map bounding box' link. Manual input of the `bounding_box` parameter
in the address box also works.

As usual, pressing the filter or paging link will reload a page with new parameters. The map keeps its position
for standard static Django filters and pager using permalink.

## Customizing view

The geodata shown on the map is represented as GeoJSON feature collection. Every GeoJSON feature corresponds to one geo field of one Django
model instance. All standard Django geometry-based fields are shown on the map by default. Every such feature has the following
list of mandatory properties to be used:

- `field` identifies the geometry field shown
- `app_label` and `model_name` identify the model of the instance shown
- `pk` is an instance primary key which identifies the model instance shown

The following optional GeoJSON feature properties are used to customize the look and feel of the feature on the map:

- `popup` if present, is used to create a popup. A value started with '<' is used to create an HTML popup,
  else the text popup is used, see also [bindPopup method](https://leafletjs.com/reference-1.7.1.html#layer-bindpopup)
- `tooltip` if present, is used to create a tooltip. A value started with '<' is used to create an HTML tooltip,
  else the text tooltip is used, see also [bindTooltip method](https://leafletjs.com/reference-1.7.1.html#layer-bindtooltip)
- `line_style` if present, is used to apply as an `options` parameter when creating lines and polygons, see also Leaflet [Path options](https://leafletjs.com/reference-1.7.1.html#path-option)
- `point_style` if present, is used as an `options` parameter to create a Leaflet marker, see also [Marker options](https://leafletjs.com/reference-1.7.1.html#marker)
- an `icon` member of the `point_style` if present, is used as an `options` parameter to create a Leaflet icon, see also [Icon options](https://leafletjs.com/reference-1.7.1.html#icon)

The Admin class may override every part of this data, or even the whole data output overriding admin methods producing this data:

- `get_geojson_feature_list(request, queryset)` returns the whole GeoJSON `FeatureList` instance representing a `queryset`
- `get_geojson_features(request, o, queryset)` returns the `features` member of the `FeatureList` instance for the model instance `o`
- `get_geojson_geometry_fields(request, o, queryset)` returns a list of geometry field names that need to be included in the feature list
- `get_geojson_feature(request, name, o, queryset)` returns a GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_geometry(request, name, o, queryset)` returns a `geometry` member of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_properties(request, name, o, queryset)` returns a `properties` member of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_feature_popup(request, name, o, queryset)` returns a `popup` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_feature_tooltip(request, name, o, queryset)` returns a `tooltip` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_feature_verbose_name(request, name, o, queryset)` returns a verbose name of the instance `o` geometry field `name` which is used to create popup and tooltip
- `get_geojson_feature_line_style(request, name, o, queryset)` returns a `line_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_feature_point_style(request, name, o, queryset)` returns a `point_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
- `get_geojson_feature_icon_style(request, name, o, queryset)` returns an `icon` member of the `point_style` property of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`
