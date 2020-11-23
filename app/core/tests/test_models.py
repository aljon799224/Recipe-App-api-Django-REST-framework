from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """TEst creating a new user with email success!"""
        email = "aljonmendiola799224@yahoo.com"
        password = "testing1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email of new user normalized"""
        email = 'aljonmendiola@YAHOO.com'
        user = get_user_model().objects.create_user(email, 'testing1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid(self):
        """test the email user if it is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_uper_user(self):
        """test create a new super user"""
        user = get_user_model().objects.create_superuser(
            "aljonmendiola@yahoo.com",
            "testing1234"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
