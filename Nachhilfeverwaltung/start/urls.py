from django.urls import include, path
from django.contrib import admin

from start.views import home
from start.views import register

urlpatterns = [
    path('', home.login_user, name='home'),
    path('register/', register)
]