import json
import datetime
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.core.files.images import ImageFile
from .models import Customer

client = APIClient()

class AccountTests(APITestCase):
    def test_registration_and_login(self):
        """
        testcase to test registration and login functionlity
        """
        # registration
        url = reverse('accounts:register')
        data = {
            'username': 'test_customer',
            'email': 'test_customer@gmail.com',
            'password': 'Tes@1234',
            'date_of_birth': '2002-01-01' 
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().username, 'test_customer')

        # login
        url = reverse('accounts:login')
        data = {
            'username': 'test_customer',
            'password': 'Tes@1234'
        }
        response = self.client.post(url, data, format='json')
        response_body = json.loads(response.content.decode('utf=8'))
        token = response_body.get('token', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(token, None)

    def test_birthdate_validation(self):
        """
        Checking future date is not valid
        """
        data = {
            'username': 'test_customer2',
            'email': 'test_customer2@gmail.com',
            'password': 'Tes@1234',
            'date_of_birth': '2000-01-01'
        }
        customer = Customer.objects.create(**data)

        update_kwargs = {'pk':customer.pk}  
        url = reverse('accounts:customer_update', kwargs=update_kwargs)

        # testing with future date
        future_date = datetime.date.today() + datetime.timedelta(days=2)
        future_date = future_date.strftime('%Y-%m-%d')
        data = {
            'date_of_birth': future_date
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(future_date, customer.date_of_birth)

        # testing with past date
        past_date = datetime.date.today() - datetime.timedelta(days=2)
        past_date = past_date.strftime('%Y-%m-%d')
        data = {
            'date_of_birth': past_date
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_body = json.loads(response.content.decode('utf=8'))
        self.assertEqual(past_date, response_body["date_of_birth"])
        
    def test_profile_photo_validation(self):
        """
        Checking uploaded image size is less then 2 MB
        """
        data = {
            'username': 'test_customer2',
            'email': 'test_customer2@gmail.com',
            'password': 'Tes@1234',
            'date_of_birth': '2000-01-01'
        }
        customer = Customer.objects.create(**data)

        update_kwargs = {'pk':customer.pk}  
        url = reverse('accounts:customer_update', kwargs=update_kwargs)

        # testing with future date
        profile_photo = ImageFile(open('static/2_mb_plus_img.jpg', 'rb'))
        data = {
            'profile_photo': profile_photo
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertNotEqual(profile_photo, customer.profile_photo)

        # testing with past date
        profile_photo = ImageFile(open('static/2_mb_below_img.jpg', 'rb'))
        data = {
            'profile_photo': profile_photo
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response_body = json.loads(response.content.decode('utf=8'))
        # self.assertEqual(past_date, response_body["date_of_birth"])

