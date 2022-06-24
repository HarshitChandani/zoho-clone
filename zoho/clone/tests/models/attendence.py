from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

from clone.models import (
    Attendence
)


class DatesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='admin', email="admin@gmail.com", first_name="harshit", last_name="chandani")
        cls.user.set_password("admin")
        cls.user.save()

    def setUp(self):
        Attendence.objects.create(
            user=self.user,
            date="2022-06-17",
            checkin_time="10:07:46",
            checkout_time="18:41:08",
            ttl_work_time="08:33:22"
        )
        Attendence.objects.create(
            user=self.user,
            date="2022-06-16",
            checkin_time="10:07:46",
            checkout_time="17:41:08",
            ttl_work_time="07:33:22"
        )

    def test_attendence_dates(self):
        self.assertSequenceEqual(
            Attendence.objects.dates('date', "year"),
            [
                date(2022, 1, 1)
            ]
        )

        self.assertSequenceEqual(
            Attendence.objects.dates("date", "month"),
            [
                date(2022, 6, 1)
            ]
        )
        self.assertSequenceEqual(
            Attendence.objects.dates("date", "day"),
            [
                date(2022, 6, 16),
                date(2022, 6, 17)
            ]
        )

    def test_attendence_dates_fails_when_given_invalid_field_argument(self):
        with self.assertRaisesMessage(
            FieldError,
            'Cannot resolve keyword "invalid_field" into field.'
        ):
            Attendence.objects.dates('invalid_field', 'year')

    def test_attendence_dates_fails_when_given_invalid_kind_argument(self):

        with self.assertRaisesMessage(ValueError, " 'kind' must be of 'year','month','day' "):
            Attendence.objects.dates('date', 'bad_kind')


