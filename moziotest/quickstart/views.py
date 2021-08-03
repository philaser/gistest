from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Point
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response

from moziotest.quickstart.serializers import UserSerializer, GroupSerializer, ProviderSerializer, LocationSerializer
from moziotest.quickstart.models import Location, Provider
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows location data to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        try:
            if user:
                return Location.objects.filter(provider=user.provider)
        except Exception:
            return Location.objects.all()


    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider)

    @action(detail=False, methods=['get'])
    def locate(self, request, *args, **kwargs):
        query_params = request.query_params
        point = Point(float(query_params['lat']),float(query_params['long']))
        locations = Location.objects.filter(polygon__contains=point).values('name','price','provider')

        return Response(locations)