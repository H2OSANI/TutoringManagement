from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from start.views import home, ueber_uns, dashboard, settings_user_password, settings_user, taking_lessons, giving_lessons, chat, giving_lessons_delete, logout_user, manage_students, manage_students_delete, admin_dashboard, admin_dashboard_delete, admin_dashboard_settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate


class TestUrls(TestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_about_us_resolves(self):
        url = reverse('ueber_uns')
        self.assertEquals(resolve(url).func, ueber_uns)

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_settings_url_resolves(self):
        url = reverse('settings-user')
        self.assertEquals(resolve(url).func, settings_user)
    
    def test_taking_lessons_url_resolves(self):
        url = reverse('taking-lessons')
        self.assertEquals(resolve(url).func, taking_lessons)
    
    def test_giving_lessons_url_resolves(self):
        url = reverse('giving-lessons')
        self.assertEquals(resolve(url).func, giving_lessons)

    def test_giving_lessons_url_resolves(self):
        url = reverse('giving-lessons')
        self.assertEquals(resolve(url).func, giving_lessons)

    def test_chat_url_resolves(self):
        url = reverse('chat', args=['1'])
        self.assertEquals(resolve(url).func, chat)
    
    def test_giving_lessons_delete_url_resolves(self):
        url = reverse('giving_lessons_delete', args=['1'])
        self.assertEquals(resolve(url).func, giving_lessons_delete)

    def test_logout_url_resolves(self):
        url = reverse('logout-user')
        self.assertEquals(resolve(url).func, logout_user)

    def test_manage_students_url_resolves(self):
        url = reverse('manage_students')
        self.assertEquals(resolve(url).func, manage_students)

    def test_manage_students_delete_url_resolves(self):
        url = reverse('manage_students_delete', args=['1'])
        self.assertEquals(resolve(url).func, manage_students_delete)

    def test_admin_dashboard_url_resolves(self):
        url = reverse('admin_dashboard')
        self.assertEquals(resolve(url).func, admin_dashboard)

    def test_admin_dashboard_delete_url_resolves(self):
        url = reverse('admin_dashboard_delete', args=['1'])
        self.assertEquals(resolve(url).func, admin_dashboard_delete)

    def test_admin_dashboard_settings_url_resolves(self):
        url = reverse('admin_dashboard_settings')
        self.assertEquals(resolve(url).func, admin_dashboard_settings)