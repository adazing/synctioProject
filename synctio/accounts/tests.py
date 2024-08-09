import profile
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user_a =User(username="hello", email="hello@something.com", password="mwahaha")
        user_a.is_staff=True
        user_a.is_superuser=True
        user_a.save()
        profile_a=Profile(user=user_a, date_of_birth="10/23/2008",streak=0)
    def test_user_exists(self):
        user_count=User.objets.all().count()
        self.assertEqual(user_count,1)
        self.assertNotEqual(user_count,0)
