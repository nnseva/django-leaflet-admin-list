from __future__ import absolute_import, print_function

import json
import re

from tests.models import DeliveryJob, Waypoint

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import Client, TestCase


class ModuleTest(TestCase):
    maxDiff = None

    def setUp(self):
        """Sets the test environment"""
        self.user = User.objects.create(username='user', is_superuser=True, is_staff=True)
        self.user.set_password('password')
        self.user.save()

        self.waypoints = [
            Waypoint.objects.create(
                name='Waypoint Test %s' % i,
                waypoint=Point([50 + i / 100, 50 + (10 - i) / 100 + 0.5])
            )
            for i in range(1, 10)
        ]

        self.delivery_jobs = [
            DeliveryJob.objects.create(
                name='Delivery Test %s' % i,
                pickup_point=Point([50 + i / 100, 50 + (10 - i) / 100]),
                dropoff_point=Point([50 + (10 - i) / 100, 50 + i / 100]),
                kind='wood',
            )
            for i in range(1, 10)
        ]

    def test_001_admin_page_map(self):
        """Test whether the map is present on the changelist view"""
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/admin/tests/waypoint/')
        self.assertIn('<div id="leaflet_admin_list_map"', response.content.decode('utf-8'))

    def test_002_admin_page_filter(self):
        """Test whether the bounding box filter is present on the changelist view"""
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/admin/tests/waypoint/')
        self.assertIn('<ul class="bounding_box_filter"', response.content.decode('utf-8'))

    def test_003_admin_page_feature_list(self):
        """Test whether the feature collection is rendered directly on the changelist view"""
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/admin/tests/waypoint/')
        self.assertIn('js = {"type": "FeatureCollection", "features": [', response.content.decode('utf-8'))

    def test_004_admin_page_bounding_box_filter_works(self):
        """Test whether the bounding box filter works"""
        c = Client()
        c.login(username='user', password='password')
        wp = self.waypoints[3]
        b = wp.waypoint.coords
        bb = (b[0] - 0.0001, b[1] - 0.0001, b[0] + 0.0001, b[1] + 0.0001)
        js = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [50.04, 50.56]},
                    "properties": {
                        "field": "waypoint", "app_label": "tests", "model_name": "waypoint", "pk": 31,
                        "popup": '<div><a title="View/Edit Waypoint" href="/admin/tests/waypoint/31/change/"><b><i>Waypoint Test 4</i></b></a></div>',
                        "tooltip": "Waypoint Test 4: Waypoint", "line_style": {"color": "#A0A0A0", "fillColor": "#A0A0A0"}
                    }
                }
            ]
        }
        response = c.get('/admin/tests/waypoint/?bounding_box=%s,%s,%s,%s' % bb)
        content = response.content.decode('utf-8')
        self.assertIn(json.dumps(js), content)
        self.assertRegex(content, r'<a href="[^>].*>Waypoint Test 4</a>')
        self.assertRegex(content, r'<p class="paginator">(.|\n)*1 Waypoint(.|\n)*</p>')

    def test_005_admin_page_works_with_nulls(self):
        dj_null_all = DeliveryJob.objects.create(
            name='Delivery Test All Null',
            kind='oil',
        )
        dj_null_pickup = DeliveryJob.objects.create(
            name='Delivery Test Dropoff Null',
            pickup_point=Point(61, 61),
            kind='oil',
        )
        dj_null_dropoff = DeliveryJob.objects.create(
            name='Delivery Test Pickup Null',
            dropoff_point=Point(71, 71),
            kind='oil',
        )

        c = Client()
        c.login(username='user', password='password')
        response = c.get('/admin/tests/deliveryjob/')
        content = response.content.decode('utf-8')
        match = re.search(r'({"type": "FeatureCollection", "features":[^;]*);', content)
        self.assertIsNotNone(match)
        js = json.loads(match.group(1))
        self.assertIn('features', js)
        self.assertEqual(len(js['features']), len(self.delivery_jobs) * 2 + 2)
        self.assertEqual(len([f for f in js['features'] if f['properties']['tooltip'] == "Delivery Test Dropoff Null: Pickup Point"]), 1)
        self.assertEqual(len([f for f in js['features'] if f['properties']['tooltip'].startswith(dj_null_pickup.name)]), 1)
        self.assertEqual(len([f for f in js['features'] if f['properties']['tooltip'].startswith(dj_null_dropoff.name)]), 1)
        self.assertEqual(len([f for f in js['features'] if f['properties']['tooltip'].startswith(dj_null_all.name)]), 0)
