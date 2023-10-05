import datetime
from start.forms import editUser, messageInput
from start.models import Person_Detail, Nachhilfe, Teilnahme, Sender, Settings_Content
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    admin = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            user_authenticated = User.objects.get(username=user.get_username())
            if User.objects.get(pk=user_authenticated.pk).groups.filter(name="Admin").exists():
                admin=True
            try:
                user_detail = Person_Detail.objects.get(pk=user.pk)
            except ObjectDoesNotExist:
                #Creating Relational Table for first Login Users
                user_detail = Person_Detail.objects.create(user_id=user.pk)
            login(request, user)
            if admin:
                return redirect('admin_dashboard')
            else:
                return redirect('/dashboard')
        else:
            messages.error(request, "Falsche Anmeldeinformationen. Bitte versuchen Sie es erneut.")
            return redirect('home')
       
    return render(request, 'Login/index.html', {
        'currentPath': request.get_full_path
    })

def dashboard(request):
    try:
        user_detail = Person_Detail.objects.get(pk=request.user.pk)

        # Counts für Anzahl-Kacheln am Dashboard
        lessons_taken = Teilnahme.objects.filter(person_ID_id=request.user.pk).count()
        lessons_given = Nachhilfe.objects.filter(person_ID_id=request.user.pk).count()

        # Bevorstehende Nachhilfen anzeigen
        taken_nachhilfe_list=Teilnahme.objects.filter(person_ID=request.user.id).select_related('person_ID').filter(Q(nachhilfe_ID__in=Nachhilfe.objects.all()))
        return render(request, 'Dashboard/index.html', {'taken_nachhilfe_list': taken_nachhilfe_list, 'lessons_taken': lessons_taken, 'lessons_given': lessons_given})
    except:
        user_detail = Person_Detail.objects.create(user_id = request.user.pk, klasse="", profile_picture="default.png")
    context = {
        'profileImage' : user_detail.profile_picture,
    }
    return render(request, 'Dashboard/index.html', context=context)

def settings_user(request):
    user = request.user
    user_detail = Person_Detail.objects.get(pk=user.pk)
    user_data = User.objects.get(pk = request.user.id)
    user_edit_form = editUser(initial={'first_name': user_data.first_name,
                                        'last_name': user_data.last_name,
                                        'email': user_data.email,
                                        'klasse': user_detail.klasse})
    
    is_Teacher = user.groups.filter(name = "Lehrer").exists()
    
    context= {
        "isTeacher": is_Teacher,
        "userform": user_edit_form
    }
    if request.method == "POST":
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        if not is_Teacher:
            user_detail.klasse = request.POST["klasse"]
            user_detail.save()
        user.save()
        messages.success(request, "Profil wurde erfolgreich aktualisiert")
        return redirect('settings_user')
    else:
        return render(request, 'Dashboard/settings.html', context=context)

def chat(request, id):
    # Chat Partner
    par_user = User.objects.get(pk = id)
    # User
    user = request.user
    message_form = messageInput

    # Fist time writing creating init message to load chat prop.
    init_message_load = Sender.objects.filter(Q(empfaenger_ID = par_user)& Q(person_ID = user))
    if bool(init_message_load) == False:
        if id != 1:
            current_date_time_init = datetime.datetime.now()
            Sender.objects.create(message = "", time = current_date_time_init, person_ID = user, empfaenger_ID = par_user)

    # List of all users who have sent messages to the logged-in user or whom the logged-in user has sent messages to
    list_user = []
    list_chat = Sender.objects.filter(
        Q(person_ID = user) | 
        Q(empfaenger_ID = user)
    ).order_by('-time')
    # Collection of the user ID's of the chats that have been loaded
    for i in list_chat:
        list_user.append(i.empfaenger_ID)
        list_user.append(i.person_ID)
    
    # Cleanup doublets
    list_user = list(dict.fromkeys(list_user))

    # Collection of the logged in user chats
    chats = {}

    # Collect all users
    for i in list_user:
        # Loading each individual chat that is associated with the user either as the sender or the recipient
        chat = Sender.objects.filter(
            Q(person_ID__in = (i, user.id)) & 
            Q(empfaenger_ID__in = (i, user.id))
            ).order_by('time')
        
        # Adding only those users that do not match the logged-in user
        if i != user:
            # Count unread messages
            counttab = Sender.objects.filter(
                Q(person_ID = i) &
                ~Q(message = "") &
                Q(empfaenger_ID = user.id) &
                Q(newmessageflag = True)
                )
            # Sender object to int
            newmesscount = counttab.count()

            # Set dictionary
            chats[chat] = {"user": i, "count": newmesscount}
        
    # Update unread messages
    Sender.objects.select_for_update().filter(
        Q(empfaenger_ID = user.id)
        ).update(newmessageflag = False)

    if request.method == "POST":
        # Load message
        message_value = request.POST["message"]
        # Get message date
        current_date_time = datetime.datetime.now()
        
        # Load messages which are not empty
        if message_value:
            Sender.objects.create(message = message_value, time=current_date_time, person_ID = user, empfaenger_ID = par_user)
        context = {
            'par_user': par_user,
            'user': user,
            'chats': chats,
            'messageform': message_form
            }
            
        return render(request, 'Dashboard/chat.html', context=context)
    else:
        context = {
            'par_user': par_user,
            'user': user,
            'chats': chats,
            'messageform': message_form,
            }
        return render(request, 'Dashboard/chat.html', context=context)


def logout_user(request):
    logout(request)
    messages.success(request, "Sie wurden erfolgreich abgemeldet.")
    return redirect('home')

def ueber_uns(request):
    ueber_uns_value=Settings_Content.objects.filter()[:1].get()
    return render(request, 'ueber_uns.html', {'ueber_uns_value': ueber_uns_value})