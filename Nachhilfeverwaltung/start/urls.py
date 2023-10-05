from django.urls import path
from django.conf.urls import handler404
from start.views import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ueber_uns/', views.ueber_uns, name='ueber_uns'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/', views.settings_user, name='settings_user'),
    path('dashboard/settings/password', views.settings_user_password.as_view(template_name='Dashboard/password.html'), name='settings_user_password'),
    path('dashboard/takinglessons/', views.taking_lessons, name='taking_lessons'),
    path('dashboard/givinglessons/', views.giving_lessons, name='giving_lessons'),
    path('dashboard/chat/<int:id>', views.chat, name='chat'),
    path('dashboard/givinglessons/giving_lessons_delete/<int:id>', views.giving_lessons_delete, name='giving_lessons_delete'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('dashboard/schuelermanagement/', views.manage_students, name='manage_students'),
    path('dashboard/schuelermanagement/manage_students_delete/<int:id>', views.manage_students_delete, name='manage_students_delete'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user_delete/<int:id>', views.admin_dashboard_delete, name='admin_dashboard_delete'),
    path('admin-dashboard/settings/', views.admin_dashboard_settings, name='admin_dashboard_settings'),
    path('api', views.NachhilfeApiView.as_view()),
]

handler404="start.views.views.error_404"
