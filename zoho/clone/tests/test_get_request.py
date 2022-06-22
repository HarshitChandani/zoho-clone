from django.test import TestCase
from django.urls import reverse

from clone.models import TimeTracker


class TestTimeTracker(TestCase):

   @classmethod
   def setUpTestData(cls):
      pass

   def test_get_time_tracker_data(self):
      response = self.client.get(reverse('zoho:time-tracker'))
   