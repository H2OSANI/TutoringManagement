import datetime
from start.forms import NachhilfeForm, TakeNachhilfeForm
from dateutil.parser import parse
from start.models import Person_Detail, Nachhilfe, Teilnahme
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.contrib import messages

def giving_lessons(request):
    formcheck = True
    user_klasse = Person_Detail.objects.get(pk = request.user).klasse
    try:
        user_klasse_val = int(user_klasse[:-1])
    except:
        user_klasse_val = False
    nachhilfe = Nachhilfe.objects.filter(person_ID = request.user.id)
    if request.method == "POST":
        if user_klasse_val == False:
            messages.error(request, "Lehrer können keine Nachhilfe geben")
            return HttpResponseRedirect(reverse('giving_lessons')) 
        try:
            form = NachhilfeForm(request.POST, user = request.user.id)
        except ObjectDoesNotExist:
            messages.error(request, "Fehler")
            return HttpResponseRedirect(reverse('giving_lessons'))
        if form.is_valid():
            grade_from = form.cleaned_data.get('klasse_von')
            grade_to = form.cleaned_data.get('klasse_bis')
            if grade_from > grade_to:
                messages.error(request, "von bis beachten...")
                formcheck = False
            if grade_to > user_klasse_val:
                messages.error(request, "Du kannst keinem Schueler Nachhilfe geben, der sich in einer hoeheren Jahrgangsstufe befindet.")
                formcheck = False
            if formcheck == True:
                try:
                    form.save()
                except:
                    messages.error(request, "Fehler")
                    return HttpResponseRedirect(reverse('giving_lessons')) 
                return HttpResponseRedirect(reverse('giving_lessons'))
            else:
                messages.error(request, "Falsche Eingaben!") 
        else:
            print("form is not Valid")
        
        return HttpResponseRedirect(reverse('giving_lessons'))
    else:
        form = NachhilfeForm(user=request.user.id)
        context = {
            'Form': form,
            'nachhilfe': nachhilfe,
        }
        return render(request, 'Dashboard/giving_lessons.html', context=context)

def taking_lessons(request):
    nachhilfe = Nachhilfe.objects.exclude(person_ID = request.user.id)
    if request.method == "POST":
        try:
            data = {'nachhilfe_ID': request.POST.get('nachhilfe_ID'), 'person_ID': request.user.id, 'datum_uhrzeit': request.POST.get('datum_uhrzeit')}
            form = TakeNachhilfeForm(data)
        except ObjectDoesNotExist:
            messages.error(request, "Fehler")
            return HttpResponseRedirect(reverse('taking_lessons'))
        if form.is_valid(): 
            date_time_check = form.cleaned_data.get('datum_uhrzeit')
            current_date_time = datetime.datetime.now() 
            
            # check the instance in order to avoid the following error: 'Parser must be a string or character stream, not datetime
            if isinstance(date_time_check, str):
                mdate = parse(date_time_check)
            else:
                mdate = date_time_check
            
            # Comparison of the date/time specified in the interface with the current date/time
            if mdate.replace(tzinfo=None) >= current_date_time.replace(tzinfo=None):
                try:
                    form.save()
                    messages.success(request, "Nachhilfe wurde erfolgreich gebucht.")
                except:
                    messages.error(request, "Fehler, Nachhilfe konnte nicht gebucht werden. Bitte Eingaben prüfen!")
                return HttpResponseRedirect(reverse('taking_lessons'))
            else:
                messages.error(request, "Vergangene Nachhilfen können nicht gebucht werden")     
                return HttpResponseRedirect(reverse('taking_lessons'))           
        else:
            print("form is not Valid")
        return HttpResponseRedirect(reverse('taking_lessons'))
        
    else:
        form = TakeNachhilfeForm(request.GET)
        context = {
            'Form': form,
            'nachhilfe': nachhilfe,
        }
        return render(request, 'Dashboard/taking_lessons.html', context=context)

def giving_lessons_delete(request, id):
    Nachhilfe.objects.filter(pk = id).delete()
    return HttpResponseRedirect(reverse('giving_lessons'))

def taking_lessons_activate(request, id):
    Teilnahme.objects.filter(pk = id).add()
    return HttpResponseRedirect(reverse('taking_lessons'))