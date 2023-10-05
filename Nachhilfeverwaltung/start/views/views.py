from start.views import teacherManageStudents, adminDashboard, student, user
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from start.forms import  TeilnahmeSerializer, NachhilfeSerializer, PasswordChangingForm
from start.decorators import allowed_users
from start.models import Teilnahme
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

#404 Page for unresolved URL´s
def error_404(request,exception):
    return render(request, '404.html')

#Login
def home(request):
    return user.home(request)

#Dashboard
@login_required(login_url='home')
def dashboard(request):
    return user.dashboard(request)


# Admindashboard Overview
@login_required(login_url='home')
@allowed_users(allowed_roles=['Admin'])
def admin_dashboard(request):
   return adminDashboard.admin_dashboard(request)
# Delete user action
@login_required(login_url='home')
@allowed_users(allowed_roles=['Admin'])
def admin_dashboard_delete(request, id):
    return adminDashboard.admin_dashboard_delete(request, id)

# Admin Dashboard CMS for static site "Über uns"
@login_required(login_url='home')
@allowed_users(allowed_roles=['Admin'])
def admin_dashboard_settings(request):
    return adminDashboard.admin_dashboard_settings(request)

# Impressum und Datenschutz anzeigen
def ueber_uns(request):
    return user.ueber_uns(request)

def logout_user(request):
    return user.logout_user(request)

#Settings for User Preferences
@login_required(login_url='home')
def settings_user(request):
    return user.settings_user(request)

# Password aendern
class settings_user_password(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('settings_user_password')


#Teacher Dashboard for managing Students
@login_required(login_url='home')
@allowed_users(allowed_roles=['Lehrer'])
def manage_students(request):
    return teacherManageStudents.manage_students(request)

#Function to remove students from giving lessons
@login_required(login_url='home')
@allowed_users(allowed_roles=['Lehrer'])
def manage_students_delete(request, id):
    return teacherManageStudents.manage_students_delete(request, id)

#Provide lessons
@login_required(login_url='home')
def giving_lessons(request):
   return student.giving_lessons(request)

# Taking lessons
# Implement a solution using a form, as Django does not have built-in functionality to allow for selection of a radio button within a list and retrieve its ID
@login_required(login_url='home')
def taking_lessons(request):
   return student.taking_lessons(request)

# Chat to communicate with other users
@login_required(login_url='home')
def chat(request, id):
   return user.chat(request, id)

@login_required(login_url='home')
#Function to remove nachhilfe
def giving_lessons_delete(request, id):
    return student.giving_lessons_delete(request, id)


@login_required(login_url='home')
#Function to take/activate nachhilfe
def taking_lessons_activate(request, id):
    return student.taking_lessons_activate(request, id)

class NachhilfeApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all teilnahme items
        '''
        teilnahme = Teilnahme.objects.filter(person_ID = request.user.id)
        serializer = TeilnahmeSerializer(teilnahme, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 2. Add a Lesson
    def post(self, request, *args, **kwargs):
        '''
        Create a lesson with given lesson data
        '''
        data = {
            'fach_ID': request.data.get('fach_ID'), 
            'preis': request.data.get('preis'),
            'klasse_von': request.data.get('klasse_von'),
            'klasse_bis': request.data.get('klasse_bis'),
            'person_ID': request.user.id
        }
        serializer = NachhilfeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)