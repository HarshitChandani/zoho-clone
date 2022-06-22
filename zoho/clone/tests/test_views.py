# This file contains the test cases to test the post request generated in the project.

# Django import
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Local import
from clone.models import (
   LeaveType,
   LeavesCreateModel
)


class TestLeaveApplicationForm(TestCase):

   @classmethod
   def setUpTestData(cls):
      LeaveType.objects.create(name='paid leave',timestamp=timezone.now())
      LeaveType.objects.create(name='unpaid leave',timestamp=timezone.now())

   def test_create_leave(self):
      data = {
         'title' :'Sister wedding',
         'leave_type': LeaveType.objects.get(id=2),
         'from-date':'2022-06-20',
         'to-date':'2022-06-21',
         'leave-reason':' '
      }
      response = self.client.post('/apply-leave/',data=data)
      self.assertEqual(LeavesCreateModel.objects.count(),1)
      

class TestLoginForm(TestCase):
   
   @classmethod
   def setUpTestData(cls) -> None:
      cls.user = User.objects.create(username='admin',email='admin@gmail.com',is_staff=True,is_active=True,is_superuser=True)
      cls.user.set_password('admin')
      cls.user.save()

   def setUp(self):
      self.login_url = reverse('zoho:login')
      self.login_credentials = {
         'username':'admin',
         'password':'admin'
      }

   def test_login_success(self):
      response = self.client.post(self.login_url,self.login_credentials,format='text/html',follow=True)
      self.assertEqual(response.status_code,200)
      
   def test_cantlogin_with_no_password(self):
      response= self.client.post(self.login_url,{'username':'admin','password':''},format='text/html')
      self.assertEqual(response.status_code,401)
   
   def test_user_is_authenticated(self):
      user = User.objects.get(email='admin@gmail.com')
      self.assertTrue(user.is_authenticated)


class TestRedirects(TestCase):

   def setUp(self):
      self.user = User.objects.create(username='admin',email='admin@gmail.com',is_superuser=True,is_active=True,is_staff=True)
      self.user.set_password('admin')
      self.user.save()

   def test_redirect_if_not_logged_in(self):
      response = self.client.get(reverse('zoho:home'))
      self.assertRedirects(response,'/login/?next=/home/')
   
   def test_logged_in_uses_correct_template(self):
      self.client.login(username='admin',password='admin')
      response = self.client.get(reverse('zoho:home'))
      
      # check if user is logged in
      self.assertEqual(str(response.context['user']),'admin')
      self.assertEqual(response.status_code,200)
      self.assertTemplateUsed(response,'home.html')