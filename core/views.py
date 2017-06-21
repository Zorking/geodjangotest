from django.contrib import messages
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render, redirect
from geopy.geocoders import GoogleV3

from core import forms, models
from geodjangotest.settings import GOOGLE_MAP_API_KEY

def geocode_address(address):
    geo_locator = GoogleV3()
    return geo_locator.geocode(address)


def get_shops(longitude, latitude):
    current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    distance_from_point = {'km': 1000}
    shops = models.Shop.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
    shops = shops.distance(current_point).order_by('distance')
    return shops.distance(current_point)


def home(request):
    form = forms.AddressForm()
    shops = []
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                address, (latitude, longitude) = location
                shops = get_shops(longitude, latitude)
    context = {'form': form, 'shops': shops}
    return render(request, 'home.html', context)


def create_shop(request):
    form = forms.ShopCreateForm()
    if request.POST:
        form = forms.ShopCreateForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.location = form.cleaned_data['location']
            shop.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create_shop.html', context)


def draw_polygons(request):
    if request.POST:
        for poly in request.POST:
            if 'poly' in poly:
                models.Polygon.objects.create(name=poly, polygon=request.POST.get(poly))
        messages.success(request, 'New polygons are successfully created')
    context = {'polygons': models.Polygon.objects.all().count(),
               'api_key': GOOGLE_MAP_API_KEY}
    return render(request, 'draw_polygons.html', context)
