from django.test import TestCase
from sign.models import Read
# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Read.objects.create()