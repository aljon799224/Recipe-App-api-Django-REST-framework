from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users api in (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid_success(self):
        """testing creating user with valid payload is successful"""
        payload = {
            'email': 'aljon@yahoo.com',
            'password': 'testing1234',
            'name': 'Aljon Mendiola'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating user is already exists"""
        payload = {
            'email': 'aljon1234@yahoo.com',
            'password': 'pw',
            'name': 'Test',
            }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'aljon1234@yahoo.com',
            'password': 'pw',
            'name': 'Test',
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that is token is created for the user"""
        payload = {'email': 'aljon@yahoo.com', 'password': 'testing1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_Credentials(self):
        """Test the token not created if invalid email and password"""
        create_user(email="aljon@yahoo.com", password="testing1234")
        payload = {"email": "aljon@yahoo.com", "password": "wrong"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test token is not created if user not exists"""
        payload = {"email": "aljon@yahoo.com", "pasword": "test1234"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
