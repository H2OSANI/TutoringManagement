from django.test import TestCase
from start.models import Nachhilfe, Faecher, User, Teilnahme, Person_Detail, Personen_Faecher, Sender, Settings_Content
from datetime import datetime
from django.utils import timezone
import pytz

class TestModels(TestCase):

    def setUp(self):
        timezone.now()
        User.objects.get_or_create(id=5)
        Faecher.objects.get_or_create(id=2)

        self.faech1 = Faecher.objects.create(
            fachbezeichnung = 'Testfach'
        )

        self.person_detail1 = Person_Detail.objects.create(
            user = User.objects.get(id=5),
            klasse = 10,
            profilBild = "NULL"
        )

        self.nachhilfe1 = Nachhilfe.objects.create(
            preis = 10,
            klasse_von = 10,
            klasse_bis = 12,
            fach_ID_id = 2,
            person_ID_id = 5
        )

        self.teilnahme1 = Teilnahme.objects.create(
            person_ID_id = 5,
            nachhilfe_ID_id = 1,
            datum_uhrzeit = datetime(2022, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)	
        )

        self.person_faecher1 = Personen_Faecher.objects.create(
            person_ID_id = 5,
            fach_ID_id = 2,
            nachhilfeflag = 1
        )

        self.sender1 = Sender.objects.create(
            message = "Test Message",
            time = datetime(2022, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
            person_ID_id = 5,
            empfaenger_ID = User.objects.get(id=5),
            newmessageflag = 1
        )

        self.settings_content1 = Settings_Content.objects.create(
            impressum = "Test",
            datenschutz = "Test"
        )

    def test_person_detail_is_created(self):
        self.assertEqual(self.person_detail1, self.person_detail1)

    def test_faecher_is_created(self):
        self.assertEqual(self.faech1, self.faech1)

    def test_nachhilfe_is_created(self):
        self.assertEquals(self.nachhilfe1, self.nachhilfe1)

    def test_teilnahme_is_created(self):
        self.assertEqual(self.teilnahme1, self.teilnahme1)

    def test_person_faecher_is_created(self):
        self.assertEqual(self.person_faecher1, self.person_faecher1)
    
    def test_sender_is_created(self):
        self.assertEqual(self.sender1, self.sender1)
    
    def test_settings_content_is_created(self):
        self.assertEqual(self.settings_content1, self.settings_content1)