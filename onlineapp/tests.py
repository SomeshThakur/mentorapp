from django.test import TestCase

# Create your tests here.
from onlineapp.models import College
from onlineapp.serializer import CollegeSerializer


class CollegeTestCase(TestCase):
    def setUp(self):
        College.objects.create(name='new',location='new',acronym='new',contact='new')
        College.objects.create(name='sheetansh',location='got',acronym='cool',contact='gf')


    def test_college(self):
        self.assertEqual(CollegeSerializer(College.objects.get(name='new')).data,{'name':'new','location':'new','acronym':'new','contact':'new'})

    def test_college2(self):
        self.assertEqual(CollegeSerializer(College.objects.get(name='sheetansh')).data,
                         {'name': 'sheetansh', 'location': 'got', 'acronym': 'cool', 'contact': 'gf'})