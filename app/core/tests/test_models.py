from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """ test new user with succesful email"""
        email = "aljon@yahoo.com"
        password = "testing1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Email needs normalize"""
        email = "aljon@YAHOO.com"
        user = get_user_model().objects.create_user(email, "testing1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalide(self):
        """checck email invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testing1234')

    def test_create_super_user(self):
        """test create superuser"""
        email = 'aljon@yahoo.com'
        password = 'testing1234'
        user = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
