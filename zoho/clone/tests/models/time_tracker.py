from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from clone.models import (
    TimeTracker
)


class DatesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='admin', email="admin@gmail.com", first_name="harshit", last_name="chandani")
        cls.user.set_password("admin")
        cls.user.save()

    def setUp(self):
        TimeTracker.objects.create(
            date="2022-06-20",
            user=self.user,
            jobs=' {"job1": {"title": "zoho ", "description": "", "hour": "05:30"}, "job2": {"title": "zoho ", "description": "", "hour": "04:30"}}',
            ttl_hours="17:60"
        )
        TimeTracker.objects.create(
            date="2022-06-18",
            user=self.user,
            jobs=' {"job1": {"title": "Zoho clone", "description": "started with time tracker module", "hour": "05:45"}} ',
            ttl_hours="9:05"
        )

    def test_simple(self):

        self.assertSequenceEqual(
            TimeTracker.objects.dates('date', 'year'),
            [
                date(2022, 1, 1)
            ]
        )

        self.assertSequenceEqual(
            TimeTracker.objects.dates('date', 'month'),
            [
                date(2022, 6, 1)
            ]
        )

        self.assertSequenceEqual(
            TimeTracker.objects.dates('date', 'day'),
            [
                date(2022, 6, 18),
                date(2022, 6, 20)
            ]
        )
