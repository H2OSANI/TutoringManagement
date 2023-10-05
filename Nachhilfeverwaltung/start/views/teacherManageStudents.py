from start.forms import editStudentGivingLessons, addStudentGivingLessons
from start.models import Person_Detail, Nachhilfe, Personen_Faecher
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from start.decorators import allowed_users

def manage_students(request):
     # Edit Student´s lessons
    if  request.method == "POST" and 'user' in request.POST:
        try:
            update_Form = editStudentGivingLessons(request.POST["user"], request.POST)
        except ObjectDoesNotExist:
            messages.error(request, "Fehler")
            return HttpResponseRedirect(reverse('manage_students'))
        if update_Form.is_valid():
            user = update_Form.cleaned_data.get('user')
            try:
                updateFaecherField = update_Form.cleaned_data.get('editGivingLessons')
            except ObjectDoesNotExist: 
                Personen_Faecher.objects.select_related('fach_ID').select_for_update().filter(person_ID_id=user).update(nachhilfeflag=False)
                return HttpResponseRedirect(reverse('manage_students')) 
            Personen_Faecher.objects.select_related('fach_ID').select_for_update().filter(Q(fach_ID__in=updateFaecherField)& Q(person_ID_id=user)).update(nachhilfeflag=True)
            Personen_Faecher.objects.select_related('fach_ID').select_for_update().filter(person_ID_id=user).exclude(fach_ID__in=updateFaecherField).update(nachhilfeflag=False)
            Nachhilfe.objects.filter(person_ID=user).exclude(fach_ID__in=updateFaecherField).delete()

        else:
            messages.error(request, "⚠️ Schüler mit ID:{} konnte nicht aktualisiert werden. Wenn alle Nachhilfen entfernt werden sollen, bitte Schüler löschen".format(update_Form.cleaned_data.get('user')))
        return HttpResponseRedirect(reverse('manage_students'))
    # Add a student who is currently able to provide lessons     
    if request.method == "POST":
        form = addStudentGivingLessons(request.POST.get("addUser"), request.POST)
        if form.is_valid():
            lessons = form.cleaned_data.get('givingLessons')
            addUser = form.cleaned_data.get('addUser')
            user = User.objects.get(pk=addUser)
            if user is not None:
                for lesson in lessons:
                    personen_faecher = Personen_Faecher.objects.select_related('fach_ID').select_for_update().filter(Q(fach_ID=lesson.pk)& Q(person_ID_id=user.pk)).update(nachhilfeflag=True)
                    
            return HttpResponseRedirect(reverse('manage_students'))
        else:
            messages.error(request, "⚠️ Schüler kann nicht hinzugefügt werden. Bitte prüfe die Eingaben")
            return HttpResponseRedirect(reverse('manage_students'))
    else:
        studentId = []
        students = []
        form = addStudentGivingLessons

        # ---- Get all Students which can give lessons -----
        personen_faecher =  Personen_Faecher.objects.all().select_related("person_ID").filter(nachhilfeflag=True)
        for person in personen_faecher:
            if not person.person_ID.id in studentId:
                studentId.append(User.objects.get(pk=person.person_ID.id).id)
        for id in studentId:
            students.append({'details' : User.objects.get(pk=id),
                             'editForm' : editStudentGivingLessons(id)})

        context = {
            'students': students,
            'addForm': form,
        }
    # Search for students which can not provide lessons yet
    if request.method == "GET" and "q" in request.GET:
        result = []
        userListSearch = manage_students_search(request)

        if not userListSearch:
            messages.success(request, "⚠️ Es konnte kein Schüler für: '{}' gefunden werden".format(request.GET.get("q")))
            return render(request, 'Dashboard/teacher.html', context=context)
        for userSearch in userListSearch:
            result.append({
                "studentSearched": userSearch,
                "addForm" : addStudentGivingLessons(userSearch.pk),
                "klasse": Person_Detail.objects.get(pk=userSearch.pk).klasse
            })

        context.update ({
            "userListSearch": result,
        })
    return render(request, 'Dashboard/teacher.html', context=context)


# Search logic to search students which can not provide lessons yet
@login_required(login_url='home')
@allowed_users(allowed_roles=['Lehrer'])
def manage_students_search(request):
#Parse Form from request
    query = request.GET.get("q")
# ----- Get users from Search which are not giving lessons yet -------
    userList = User.objects.filter(Q(
        Q(first_name__icontains = query)| 
        Q(last_name__icontains = query)| 
        Q(username__icontains = query)| 
        Q(email__icontains = query))&
        ~Q(pk__in= Personen_Faecher.objects.select_related("person_ID").filter(nachhilfeflag=True).values("person_ID"))&
        ~Q(pk__in= Group.objects.select_related("user").filter(Q(name="Lehrer")| Q(name="Admin")).values("user"))&
        Q(is_superuser=False)&
        Q(is_active=True))

    return(userList)

def manage_students_delete(request, id):
    Personen_Faecher.objects.filter(person_ID = id).update(nachhilfeflag=False)
    Nachhilfe.objects.filter(person_ID = id).delete()
    return HttpResponseRedirect(reverse('manage_students'))