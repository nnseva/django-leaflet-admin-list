from setuptools import setup

from leaflet_admin_list.version import __version__ as version


with open("README.rst", "r") as fp:
    description = fp.read() + "\n"

setup(
    name="django-leaflet-admin-list",
    version=version,
    description="Django Leaflet Admin List",
    long_description=description,
    url='https://github.com/nnseva/django-leaflet-admin-list',
    author='Vsevolod Novikov',
    author_email='nnseva@gmail.com',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Development Status :: 4 - Beta',
        "Framework :: Django",
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
    keywords="django admin leaflet map list view",
    license='LGPL',
    packages=['leaflet_admin_list'],
    package_data={
        'leaflet_admin_list': [
            'templates/leaflet_admin_list/leaflet_admin_filter.html',
            'templates/leaflet_admin_list/leaflet_admin_list.html',
        ]
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django",
        "django-leaflet",
    ],
)
