from django.test import TestCase
from clone.models import Department

class TestModels(TestCase):


   # this test case is just to get hands on the test framework in django
   def test_dept_model_str(self):
      dept1 = Department.objects.create(name='BMC',emp_cnt=81)
      dept2 = Department.objects.create(name='Data Integration',emp_cnt=121)
      self.assertEqual(str(dept1),'BMC')
      self.assertEqual(str(dept2),'Data Integration')
      self.assertEqual(str(dept2),'testing')


   
