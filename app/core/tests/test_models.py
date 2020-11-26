from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="aljon@yahoo.com", password="testing1234"):
    """create sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Pork'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """test the recipe str representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Pork Steak',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
