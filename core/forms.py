from django import forms
from django.forms import ModelForm
from core.models import Shop

from django.contrib.gis import geos
from geopy.geocoders import GoogleV3


class AddressForm(forms.Form):
    address = forms.CharField()


class ShopCreateForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['location']

    def clean(self):
        cleaned_data = self.cleaned_data
        address = u'%s %s' % (cleaned_data.get('city'), cleaned_data.get('address'))
        geocoder = GoogleV3()
        location = geocoder.geocode(address)
        if not location:
            raise forms.ValidationError("This location does\'t exists")
        else:
            address, (latitude, longitude) = location
            point = "POINT(%s %s)" % (longitude, latitude)
            cleaned_data['location'] = geos.fromstr(point)
        return cleaned_data
