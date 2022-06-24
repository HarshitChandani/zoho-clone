from string import ascii_letters
from datetime import datetime,date

from django.test import TestCase
from django.contrib.auth.models import User

from clone.models import (
   EmpPersonal
)


class TestCharFields(TestCase):
   fixtures = ["emp_personal.json",'users.json']

   def test_char_in_number_field(self):
      emp_phone_nums = EmpPersonal.objects.values_list('no')
      self.assertNotIn(
         ascii_letters,
         emp_phone_nums,
         msg = 'Phone Number must not contain alphanumeric characters.'
      )

   def test_special_char_in_number_field(self):
      special_chars ='[@_!#$%^&*()<>?/\|}{~:]'  
      emp_phone_nums = EmpPersonal.objects.values_list('no')
      self.assertNotIn(
         special_chars,
         emp_phone_nums,
         msg = 'Phone Number must not contain any special characters.'
      )
   
class TestDateFields(TestCase):
   fixtures = ["emp_personal.json",'users.json']

   def test_birth_date_field_format(self):
      # TestCase to check the format of the birth date field.
      # Correct Format: YYYY-MM-DD
      birth_date = EmpPersonal.objects.get(id=1).birth_date
      self.assertEqual(
         birth_date, # The value
         date(birth_date.year,birth_date.month,birth_date.day) # The format
      )