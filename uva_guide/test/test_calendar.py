import datetime
from django.utils import timezone
from django.test import TestCase
from schedule.models import Calendar, Event


class TestCalendar(TestCase):
   
    def blank_calendar(self):
        cal = Calendar()
        self.assertEqual(list(cal.get_recent()), [])

    def test_calendar_event(self):
        cal = Calendar.objects.create()
        start = timezone.now() + datetime.timedelta(days=1)
        end = start + datetime.timedelta(hours=1)
        event = Event.objects.create(
            title="Party Time!", description="Yes", start=start, end=end, calendar=cal
        )
        cal.events.add(event)
        event = cal.events.first()
        self.assertEqual(event.start, start)
        self.assertEqual(event.end, end)
        self.assertEqual(event.description, "Yes")


