from start.forms import editAdminDashboardUser, addAdminDashboardUser, Settings_Content_Form
from django.contrib.auth.decorators import login_required
from start.decorators import allowed_users
from start.models import Faecher, Personen_Faecher, Settings_Content
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import IntegrityError

def admin_dashboard(request):
 # Load user data
    all_user_objects = User.objects.all().exclude(pk=1).order_by("first_name")
    all_users = []
    for user in all_user_objects:
        if user.is_superuser:
            all_users.append({
            "details": user,
            "editForm": editAdminDashboardUser(user.id),
            })
        else:
            all_users.append({
                "details": user,
                "editForm": editAdminDashboardUser(user.id),
                "missingLesson": True if (user.groups.filter().order_by('-id').first().name == "Schueler" and not Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(person_ID = user)))) else False,
            })
    context={
        "allUsers": all_users,
        "form": addAdminDashboardUser(),
    }
    # Submission for editing a user´s data
    if request.POST.get("form_type") == 'editForm':
        postEditForm = editAdminDashboardUser(request.POST.get("user"), request.POST, instance=User.objects.get(pk=request.POST.get('user')))
        if postEditForm.is_valid():
            postEditForm.save()
            postEditForm.updateDependencies(request.POST.get("klasse"), postEditForm.cleaned_data.get("faecher"))
            return HttpResponseRedirect(reverse('admin_dashboard'))
        else:
            messages.error(request, "❌ {}".format(postEditForm.errors.as_text()))
    # Submission for adding a new user
    if request.POST.get("form_type") == 'form':
        postForm = addAdminDashboardUser(request.POST)
        print(request.POST)
        if postForm.is_valid():
            username = postForm.cleaned_data.get('addFirst_name')
            email = postForm.cleaned_data.get('addEmail')
            lastname = postForm.cleaned_data.get('addLast_name')
            klasse = postForm.cleaned_data.get('addKlasse')
            group = postForm.cleaned_data.get('addRole')
            group = group.name
            try:
                postForm.createUser(group=group, username=username,last_name=lastname, email=email, klasse=klasse)
            except IntegrityError:
                messages.error(request, "❌ Benutzer konnte nicht erstellt werden. Er existiert möglicherweise schon")
            return HttpResponseRedirect(reverse('admin_dashboard'))
        else:
            messages.error(request, "❌ {}".format(postForm.errors.as_text()))
    # Filter the user list
    if request.method == "GET" and "q" in request.GET:
        userListSearchObj = admin_dashboard_search(request)
        userListSearch = []
        if not userListSearchObj:
            messages.success(request, "Es konnte kein Benutzer für: '{}' gefunden werden".format(request.GET.get("q")))
            return render(request, 'Admin-Dashboard/index.html', context=context)
        for userList in userListSearchObj:
            if userList.is_superuser:
                userListSearch.append({
                "details": userList,
                "editForm": editAdminDashboardUser(userList.id),
                })
            else:
                userListSearch.append({
                    "details": userList,
                    "editForm": editAdminDashboardUser(userList.id),
                    "missingLesson": True if (userList.groups.filter().order_by('-id').first().name == "Schueler" and not Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(person_ID = userList)))) else False,
                })
        context.update ({
            "allUsers": userListSearch,
        })
    
    return render(request, 'Admin-Dashboard/index.html', context=context)

def admin_dashboard_settings(request):
    if request.method == "POST":
        try:
            form = Settings_Content_Form(request.POST, instance=Settings_Content.objects.get(id=1))
        except ObjectDoesNotExist:
            messages.error(request, "Fehler")
            return HttpResponseRedirect(reverse('admin_dashboard_settings'))
        if form.is_valid():
            try:
                form.save()
            except:
                messages.error(request, "Fehler")
                return HttpResponseRedirect(reverse('admin_dashboard_settings'))   
        else:
            print("form is not Valid")
        
        return HttpResponseRedirect(reverse('admin_dashboard_settings'))

    settings_content = Settings_Content.objects.get(id=1)
    context = {"Form": Settings_Content_Form(initial={'impressum': settings_content.impressum, 'datenschutz': settings_content.datenschutz})}
    return render(request, 'admin-dashboard/settings.html', context=context)

def admin_dashboard_delete(request, id):
    User.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('admin_dashboard'))

# Search logic for filtering the user list on the admin dashboard
@login_required(login_url='home')
@allowed_users(allowed_roles=['Admin'])
def admin_dashboard_search(request):
#Parse Form from request
    query = request.GET.get("q")
# ----- Get users from Search which are not giving lessons yet -------
    userList = User.objects.filter(Q(
        Q(first_name__icontains = query)| 
        Q(last_name__icontains = query)| 
        Q(username__icontains = query)| 
        Q(email__icontains = query)
        )& ~Q(pk=1))

    return(userList)
