from string import ascii_letters

from django.test import TestCase
from django.contrib.auth.models import User

from clone.models import (
   Department
)


class TestCharField(TestCase):
   
   fixtures = ["department.json"]

   def __create_dept(self,name="BMC",emp_count=98):
      dept = Department.objects.create( name = name, emp_cnt = emp_count )
      return dept
   
   def test_initial(self):
      dept = self.__create_dept()
      self.assertEqual(dept.__str__(), dept.name)
      self.assertTrue(isinstance(dept,Department))

   def test_lookup_integer_in_charfield(self):
      self.assertEqual(Department.objects.filter(name=1).count(),0)

   def test_emoji_not_in_charfield(self):
      dept = Department.objects.all()
      dept_list = [d.name for d in dept ]
      self.assertNotIn("😀",dept_list)

   def test_lookup_char_in_intfield(self):
      emp_cnt = Department.objects.values_list('emp_cnt')
      self.assertNotIn(
         ascii_letters,
         emp_cnt,
         msg=" Integer Field should not contain characters."
      )
   
   def test_empty_char_field(self):
      self.assertNotEqual(
         Department.objects.values_list('emp_cnt'), 
         " "
      )

