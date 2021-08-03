from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from moziotest.quickstart.models import Location, Provider


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ['pk','name', 'email', 'phone', 'language', 'currency']
        lookup_field = 'username'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    provider = ProviderSerializer()

    class Meta:
        model = User
        fields = ['provider','username','password','groups']
        read_only_fields = ['username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        provider_data = validated_data.pop('provider')
        password = validated_data.pop('password')
        username = provider_data['name']
        email = provider_data['email']
        phone = provider_data['phone']
        language = provider_data['language']
        currency = provider_data['currency']
        user = User.objects.create_user(username=username, email=email, password=password)
        Provider.objects.create(user=user, name=username, email=email, phone=phone, language=language, currency=currency)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['provider']
        geo_field = "polygon"