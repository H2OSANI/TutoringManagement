from django.test import TestCase, Client
from django.urls import reverse
from start.models import Person_Detail, Nachhilfe, Faecher, Personen_Faecher, Teilnahme, Settings_Content
from django.contrib.auth.models import User, Group
import json
from django.shortcuts import get_object_or_404


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.password_change = reverse('settings-user-password')
        self.home = reverse('home')
        self.ueber_uns = reverse('ueber_uns')
        self.dashboard = reverse('dashboard')
        self.settings_user = reverse('settings-user')
        self.taking_lessons = reverse('taking-lessons')
        self.giving_lessons = reverse('giving-lessons')
        self.chat = reverse('chat', args=['1'])
        self.giving_lessons_delete = reverse('giving_lessons_delete', args=['1'])
        self.logout_user = reverse('logout-user')
        self.manage_students = reverse('manage_students')
        self.manage_students_delete = reverse('manage_students_delete', args=['1'])
        self.admin_dashboard = reverse('admin_dashboard')
        self.admin_dashboard_delete = reverse('admin_dashboard_delete', args=['1'])
        self.admin_dashboard_settings = reverse('admin_dashboard_settings')

    def test_password_change(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])

        response = self.client.get(self.password_change)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/password.html')  

    def test_home_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])

        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Login/index.html')

    def test_dashboard_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])

        response = self.client.get(self.dashboard)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/index.html')
    
    def test_ueber_uns_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        Settings_Content.objects.get_or_create(id=1, impressum="Test", datenschutz="Test")

        response = self.client.get(self.ueber_uns)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ueber_uns.html')

    def test_dashboard_settings_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        Person_Detail.objects.get_or_create(user_id = 1, klasse='10c')[0]

        response = self.client.get(self.settings_user)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/settings.html')

    def test_taking_lessons_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])

        response = self.client.get(self.taking_lessons)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/taking_lessons.html')

    def test_giving_lessons_GET(self):
        self.client.force_login(User.objects.get_or_create(username='Peter')[0])
        Person_Detail.objects.get_or_create(user_id = 1, klasse='10c')[0]

        response = self.client.get(self.giving_lessons)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/giving_lessons.html')

    def test_chat_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])

        response = self.client.get(self.chat)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/chat.html')

    def test_manage_students_GET(self):
        user = User.objects.get_or_create(username='testuser1')[0]
        my_group = Group.objects.get_or_create(name='Lehrer')[0]
        my_group.user_set.add(user)
        self.client.force_login(user)

        response = self.client.get(self.manage_students)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/teacher.html')

    def test_admin_dashboard_GET(self):
        user = User.objects.get_or_create(username='testuser1')[0]
        my_group = Group.objects.get_or_create(name='Admin')[0]
        my_group.user_set.add(user)
        self.client.force_login(user)        

        response = self.client.get(self.admin_dashboard)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Admin-Dashboard/index.html')

    def test_admin_dashboard_settings_GET(self):
        user = User.objects.get_or_create(username='testuser1')[0]
        my_group = Group.objects.get_or_create(name='Admin')[0]
        my_group.user_set.add(user)
        self.client.force_login(user)
        Settings_Content.objects.get_or_create(id=1, impressum="Test", datenschutz="Test")

        response = self.client.get(self.admin_dashboard_settings)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-dashboard/settings.html')

