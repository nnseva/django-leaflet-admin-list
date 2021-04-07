from __future__ import absolute_import, print_function

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Waypoint(models.Model):
    """ Example """

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name'),
    )

    waypoint = models.PointField(geography=True, null=True, blank=True, verbose_name=_("Waypoint"), help_text=_("Waypoint to pass"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Waypoint')
        verbose_name_plural = _('Waypoints')


class DeliveryJob(models.Model):
    """ Example """

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name'),
    )
    quantity = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Quantity'),
    )
    weight = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Weight'),
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True, blank=True,
        verbose_name=_('Price'),
    )
    kind = models.CharField(
        max_length=32,
        choices=[
            ('wood', _('Wood')),
            ('steel', _('Steel')),
            ('oil', _('Oil')),
        ],
        verbose_name=_('Kind'),
    )

    pickup_point = models.PointField(geography=True, null=True, blank=True, verbose_name=_("Pickup Point"), help_text=_("Where to get cargo"))
    dropoff_point = models.PointField(geography=True, null=True, blank=True, verbose_name=_("Dropoff Point"), help_text=_("Where to delivery cargo"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Delivery Job')
        verbose_name_plural = _('Delivery Jobs')


class Building(models.Model):
    """ Example """

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name'),
    )
    levels = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Levels'),
    )

    geometry = models.GeometryCollectionField(geography=True, null=True, blank=True, verbose_name=_("Geometry"), help_text=_("Geometry of the building"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')
