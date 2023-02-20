"""Fix for the wrong psycopg>=2.8 value processing"""


def fix():
    """Make a fix for the wrong psycopg>=2.8 value processing"""
    import django
    if django.VERSION < (3, 1):
        from django.utils.timezone import utc
        from django.db.backends.postgresql import utils

        def utc_tzinfo_factory_fixed(offset):
            if offset:
                raise AssertionError("database connection isn't set to UTC")
            return utc
        utils.utc_tzinfo_factory = utc_tzinfo_factory_fixed
