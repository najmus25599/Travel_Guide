from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from events.models import Location,Transport,Stuff,Event,Enrollment,Review,Comment,Vote,Reply,VoteRp

from events.views import event_detail, enroll, all_events

from django.core.files.uploadedfile import SimpleUploadedFile

class UrlsTest(SimpleTestCase):
    def test_allEvent(self):
        url = reverse('events:Events')
        self.assertEquals(resolve(url).func, all_events)

   # def test_eventDetail(self):
   #     url = reverse('events:Event_details', args=['slug'])
   #     self.assertEquals((resolve(url).func, event_detail))