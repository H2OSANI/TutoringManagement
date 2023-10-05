from django.test import TransactionTestCase
from start.forms import NachhilfeForm, usersearch, addAdminDashboardUser, editAdminDashboardUser, addStudentGivingLessons, TakeNachhilfeForm, messageInput, editUser, PasswordChangingForm, Settings_Content_Form, Settings_Content
from start.models import User, Faecher, Personen_Faecher, Nachhilfe, Sender
from django.contrib.auth.models import User, Group
from datetime import datetime
from django.utils import timezone
import pytz

class TestForms(TransactionTestCase):

    # Nachhilfe Form
    def test_nachhilfe_form_valid_data(self):
        faecher = Faecher.objects.get_or_create(id=1)[0]
        user = User.objects.get_or_create(id=1)[0]
        Personen_Faecher.objects.get_or_create(id=1, fach_ID=faecher, person_ID=user, nachhilfeflag=1) 
        
        nachhilfeForm = NachhilfeForm(user=1, data={
            'fach_ID': 1,
            'preis': 39,
            'klasse_von': 10,
            'klasse_bis': 12,
            'person_ID': 1
        })

        self.assertTrue(nachhilfeForm.is_valid())

    def test_nachhilfe_form_no_data(self):
        nachhilfeForm = NachhilfeForm(user=1, data={})
        self.assertFalse(nachhilfeForm.is_valid())
        self.assertEqual(len(nachhilfeForm.errors), 5)

    # usersearch
    def test_user_search_form_valid_data(self):
        self.user1 = User.objects.get_or_create(id=1)[0]

        userSearchForm = usersearch(data={
                'user': self.user1.id
            })
        
        self.assertTrue(userSearchForm.is_valid())

    def test_user_search_form_no_data(self):
        userSearchForm = usersearch(data={})
        self.assertFalse(userSearchForm.is_valid())
        self.assertEqual(len(userSearchForm.errors), 1)


    # addAdminDashboardUser
    def test_addAdminDashboardUser_form_valid_data(self):     
        addAdminDashboardUserForm = addAdminDashboardUser(data={
            'addFirst_name': "Vorname",
            'addLast_name': "Nachname",
            'addEmail': "Email",
            'addRole': Group.objects.get_or_create(name='Admin')[0],
            'addKlasse': 10
        })

        self.assertTrue(addAdminDashboardUserForm.is_valid())
    
    def test_addAdminDashboardUser_form_no_data(self):
        addAdminDashboardUserForm = addAdminDashboardUser(data={})
        self.assertFalse(addAdminDashboardUserForm.is_valid())
        self.assertEqual(len(addAdminDashboardUserForm.errors), 4)

    # editAdminDasboardUser
#    def test_editAdminDasboardUser_form_valid_data(self):
        
#        user = User.objects.get_or_create(username='janedoe')[0]
#        my_group = Group.objects.get_or_create(name='Schueler')[0]
#        my_group.user_set.add(user)

#        editAdminDasboardUserForm = editAdminDashboardUser(userId=1, data={
#            'first_name': 'Jane',
#           'last_name': 'Doe',
#            'email': 'janedoe@example.com',
#            'username': 'janedoe',
#            'is_active': True,
#            'klasse': '12',
#            'user': 1
#        })

#        self.assertFalse(editAdminDasboardUserForm.is_valid())
#        print(editAdminDasboardUserForm.errors)
    
#    def test_editAdminDasboardUser_form_no_data(self):
#        editAdminDasboardUserForm = editAdminDashboardUser(userId=1, data={})
#        self.assertFalse(editAdminDasboardUserForm.is_valid())
#        self.assertEqual(len(editAdminDasboardUserForm.errors), 4)

    # addStudentGivingLessons
    def test_addStudentGivingLessons_form_valid_data(self):
        faecher = Faecher.objects.get_or_create(id=1)[0]
        user = User.objects.get_or_create(id=1)[0]
        Personen_Faecher.objects.get_or_create(id=1, fach_ID=faecher, person_ID=user, nachhilfeflag=1)      
        addStudentGivingLessonsForm = addStudentGivingLessons(userId=1, data={
            'givingLessons': [1],
            'addUser': 1,
        })

        self.assertTrue(addStudentGivingLessonsForm.is_valid())
    
    def test_addStudentGivingLessons_form_no_data(self):
        addStudentGivingLessonsForm = addStudentGivingLessons(userId=1, data={})
        self.assertFalse(addStudentGivingLessonsForm.is_valid())
        self.assertEqual(len(addStudentGivingLessonsForm.errors), 2)
    
    #TakeNachilfe
    def test_take_nachhilfe_form_valid_data(self):
        timezone.now()

        faecher = Faecher.objects.get_or_create(id=1)[0]
        user = User.objects.get_or_create(id=1)[0]
        Personen_Faecher.objects.get_or_create(id=1, fach_ID=faecher, person_ID=user, nachhilfeflag=1) 
        Nachhilfe.objects.get_or_create(id=1, preis=10, fach_ID=faecher, person_ID=user)[0]

        takeNachhilfeForm = TakeNachhilfeForm(data={
            'person_ID': 1,
            'nachhilfe_ID': 1,
            'datum_uhrzeit': datetime(2022, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        })

        self.assertTrue(takeNachhilfeForm.is_valid())

    def test_take_nachhilfe_form_no_data(self):
        takeNachhilfeForm = TakeNachhilfeForm(data={})
        self.assertFalse(takeNachhilfeForm.is_valid())
        self.assertEqual(len(takeNachhilfeForm.errors), 3)
    
    # message Input
    def test_message_input_form_valid_data(self):
        timezone.now()

        user = User.objects.get_or_create(id=1)[0]

        sender = Sender.objects.create(
            message = "Test Message",
            time = datetime(2022, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
            person_ID_id = 1,
            empfaenger_ID = User.objects.get(id=1),
            newmessageflag = 1
        )
    
        messageInputForm = messageInput(data={
            'message': "Test",
            'person_ID': user,
            'time': datetime(2022, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
            'empfaenger_ID': 1
        })

        self.assertTrue(messageInputForm.is_valid())

    def test_take_nachhilfe_form_no_data(self):
        messageInputForm = messageInput(data={})
        self.assertFalse(messageInputForm.is_valid())
        self.assertEqual(len(messageInputForm.errors), 3)
    
    # Edit User
    def test_edit_user_form_valid_data(self): 
        editUserForm = editUser(data={
            'first_name': "Test",
            'last_name': "jfaksldö",
            'email': "fjskadl@hfsakld.de",
            'klasse': 12
        })

        self.assertTrue(editUserForm.is_valid())

    def test_take_nachhilfe_form_no_data(self):
        editUserForm = editUser(data={})
        self.assertFalse(editUserForm.is_valid())
        self.assertEqual(len(editUserForm.errors), 1)
    
    # Passwort ändern
    # Fehler wegen altem Passwort => wie komme ich da dran?
#    def test_password_change_form_valid_data(self):
#        user = User.objects.get_or_create(id=1, username='Jo', password='testpass1234')[0]
#        passwordChangeForm = PasswordChangingForm(user, data={
#            'old_password': 'testpass1234',
#            'new_password1': 'newpass1234',
#            'new_password2': 'newpass1234'
#        })

#        self.assertFalse(passwordChangeForm.is_valid())
#        print (passwordChangeForm.errors)
    
#    def test_password_change_form_no_data(self):
#        user = User.objects.get_or_create(id=1)[0]
#        passwordChangeForm = PasswordChangingForm(user, data={})
#        self.assertFalse(passwordChangeForm.is_valid())
#        self.assertEqual(len(passwordChangeForm.errors), 3)

    # Settings_Content_Form
    def test_settings_content_form_valid_data(self):
        Settings_Content.objects.get_or_create(id=1, impressum="Test", datenschutz="Test")
        settingsContentForm = Settings_Content_Form(data={
            'impressum': 'Test',
            'datenschutz': 'Test'
        })

        self.assertTrue(settingsContentForm.is_valid())

    def test_take_nachhilfe_form_no_data(self):
        Settings_Content.objects.get_or_create(id=1, impressum="Test", datenschutz="Test")
        settingsContentForm = Settings_Content_Form(data={})
        self.assertFalse(settingsContentForm.is_valid())
        self.assertEqual(len(settingsContentForm.errors), 2)