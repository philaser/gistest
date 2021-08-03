import json
from rest_framework import status
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from moziotest.quickstart.models import Provider, Location
from moziotest.quickstart.serializers import ProviderSerializer, LocationSerializer


# initialize the APIClient app


class GetProviderTest(APITestCase):
    """ Test module for GET provider API """

    def setUp(self):
        user = User.objects.create_user(username='test_user', email='test@test.com', password='1234')
        Provider.objects.create(user=user, name='testprovider', email='test@test.com', phone='1234', language='en-Us', currency='USD')

        user2 = User.objects.create_user(username='test_user2', email='test2@test.com', password='1234')
        Provider.objects.create(user=user2, name='testprovider2', email='test2@test.com', phone='1234', language='en-Us', currency='USD')

        self.client.login(username=user.username, password='1234')

    def test_get_all_providers(self):
        # get API response
        response = self.client.get(reverse('providers-list'))
        # get data from db
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_provider(self):
        # get API response
        response = self.client.get(reverse('providers-detail', kwargs={'name': 'testprovider2'}))
        # get data from db
        provider = Provider.objects.get(pk=2)
        serializer = ProviderSerializer(provider)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_provider_invalid(self):
        # get API response
        response = self.client.get(reverse('providers-detail', kwargs={'name': 'faketestprovider'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostLocationTest(APITestCase):
    """ Test module for POST location API """

    def setUp(self):
        user = User.objects.create_user(username='test_user', email='test@test.com', password='1234')
        Provider.objects.create(user=user, name='testprovider', email='test@test.com', phone='1234', language='en-Us', currency='USD')

        user2 = User.objects.create_user(username='test_user2', email='test2@test.com', password='1234')
        Provider.objects.create(user=user2, name='testprovider2', email='test2@test.com', phone='1234', language='en-Us', currency='USD')

        self.client.login(username=user.username, password='1234')

    def test_post_location(self):
        # get API response
        data = {
                    "name": "polygonamazon33",
                    "price": 3524,
                    "polygon": {
                        "type": "Polygon",
                        "coordinates": [
                        [
                            [
                            -2.63671875,
                            10.574222078332806
                            ],
                            [
                            -1.845703125,
                            7.536764322084078
                            ],
                            [
                            0.703125,
                            6.926426847059551
                            ],
                            [
                            0.87890625,
                            10.487811882056695
                            ],
                            [
                            -2.63671875,
                            10.574222078332806
                            ]
                        ]
                        ]
                    }
                }
        response = self.client.post(reverse('locations-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_location_invalid_data(self):
        # get API response
        data = {
                    "name": "polygonamazon33",
                    "price": 3524,
                    "polygon": {
                        "type": "afg",
                        "coordinaters": [
                        [
                            [
                            -2.63671875,
                            10.574222078332806
                            ],
                            [
                            -1.845703125,
                            7.536764322084078
                            ],
                            [
                            0.703125,
                            6.926426847059551
                            ],
                            [
                            0.87890625,
                            10.487811882056695
                            ],
                            [
                            -2.63671875,
                            10.574222078332806
                            ]
                        ]
                        ]
                    }
                }
        response = self.client.post(reverse('locations-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
