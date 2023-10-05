from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Nachhilfe, Faecher, Person_Detail, Teilnahme, Personen_Faecher, User, Sender, Settings_Content
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth.forms import UserChangeForm
from rest_framework import serializers
from start.tailwind.tailwindForms import formsStyle

#Create Nachhilfe Form
class NachhilfeForm(forms.ModelForm):
    class Meta:
        model = Nachhilfe
        fields = ('fach_ID', 'preis', 'klasse_von', 'klasse_bis', 'person_ID')

    fach_ID   = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.userid = kwargs.pop("user")
        super(NachhilfeForm, self).__init__(*args, **kwargs)
        self.fields['fach_ID'].queryset = Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(Q(person_ID = self.userid)& Q(nachhilfeflag=True)).values('fach_ID')))
        self.fields['person_ID'].initial = self.userid
        self.fields['person_ID'].widget.attrs.update({'class':'hidden'})
        self.fields['person_ID'].label =  False
        self.fields['fach_ID'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['preis'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['klasse_von'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['klasse_bis'].widget.attrs.update({'class': formsStyle["field"]})

class usersearch(forms.Form):

    user = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super(usersearch, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        self.fields['user'].label =  False

class addAdminDashboardUser(forms.Form):

        addFirst_name = forms.CharField(label='Vorname', required=True, widget=forms.TextInput(attrs={'placeholder': 'Vorname'}))
        addLast_name = forms.CharField(label='Nachname', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nachname'}))  
        addEmail = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        addRole = forms.ModelChoiceField(queryset=Group.objects.all(), label="Rolle", required=True, empty_label="Rolle auswählen . . .")
        addKlasse= forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'placeholder': 'Jahrgangsstufe'}))

        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['addKlasse'].widget.attrs.update({'class': formsStyle["fieldHidden"]})
            self.fields['addFirst_name'].widget.attrs.update({'class': formsStyle["field"]})
            self.fields['addLast_name'].widget.attrs.update({'class': formsStyle["field"]})
            self.fields['addEmail'].widget.attrs.update({'class': formsStyle["field"]})
            self.fields['addRole'].widget.attrs.update({'class': formsStyle["field"]})  

        def __getGroups(self, group="", *args, **kwargs):
            match group:
                case "Admin":
                    retGroup=Group.objects.all()
                case "Lehrer":
                    retGroup=Group.objects.filter(Q(name="Schueler")| Q(name="Lehrer"))
                case _:
                    retGroup=Group.objects.get(name="Schueler")
            return retGroup

        def createUser(self, group="Schueler", username="", last_name="", email="", klasse="", *args, **kwargs):
            createdUser = User.objects.create_user(
                username="{}".format(username),
                email=email,
                password="1234{}1234".format(username.lower()))
            createdUser.first_name=username
            createdUser.last_name=last_name
            createdUser.save()
            if klasse:
                Person_Detail.objects.create(user_id=createdUser.id, klasse=klasse)
            groups = self.__getGroups(group)
            if group == "Schueler":
                createdUser.groups.add(groups)
            else:
                for object in groups:
                    createdUser.groups.add(object)
        
class editAdminDashboardUser(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_active')
    
    klasse = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'placeholder': 'Jahrgangsstufe'}))
    user = forms.IntegerField(label=False)
    faecher = forms.ModelMultipleChoiceField(queryset=Faecher.objects.all(), widget = forms.CheckboxSelectMultiple, required=False)

    def __init__(self, userId, *args, **kwargs):
        super(editAdminDashboardUser, self).__init__(*args, **kwargs)
        user = self.__getUser(userId)
        usergroup = user.groups.filter().order_by('-id').first()
        if usergroup != None:
            if usergroup.name == "Schueler":
                self.fields['klasse'].initial = Person_Detail.objects.get(pk=userId).klasse
                self.fields['klasse'].label = "Jahrgangsstufe"
                self.fields['klasse'].widget.attrs.update({'class': formsStyle["field"]})
                self.fields['faecher'].initial = Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(person_ID = userId).values('fach_ID')))
            else:
                del self.fields['faecher']
                self.fields['klasse'].widget.attrs.update({'class': 'hidden'})
                self.fields['klasse'].label = False
        else:
            self.fields['klasse'].widget.attrs.update({'class': 'hidden'})
            self.fields['klasse'].label = False
            del self.fields['faecher']
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['username'].initial = user.username
        del self.fields['password']
        self.fields['username'].help_text = None
        self.fields['is_active'].initial = user.is_active
        self.fields['is_active'].help_text = None
        self.fields['user'].initial = userId
        self.fields['user'].widget.attrs.update({'class': 'hidden'})
        self.fields['first_name'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['last_name'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['email'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['username'].widget.attrs.update({'class': formsStyle["field"]})

    def updateDependencies(self, klasse="", faecher=None, *args, **kwargs):
        updateUser = User.objects.get(pk=self.fields['user'].initial)
        if klasse:
            Person_Detail.objects.filter(pk=updateUser.id).update(klasse=klasse)
        if faecher:
            deleteFaecher = Personen_Faecher.objects.select_related('person_ID', 'fach_ID').filter(person_ID=updateUser.pk).values('fach_ID').exclude(fach_ID__in=faecher)
            for fach in faecher:
                if not  Personen_Faecher.objects.select_related('fach_ID', 'person_ID').filter(Q(fach_ID=fach.id)& Q(person_ID=updateUser.pk)):
                    Personen_Faecher.objects.create(fach_ID_id=fach.id, person_ID_id=updateUser.pk, nachhilfeflag=0)
            Personen_Faecher.objects.select_related('fach_ID', 'person_ID').filter(Q(person_ID=updateUser.pk)& Q(fach_ID__in=deleteFaecher)).delete()
            Nachhilfe.objects.filter(person_ID=updateUser.pk).exclude(fach_ID__in=deleteFaecher).delete()
        
    def __getUser(self, userId, *args, **kwargs):
        return User.objects.get(pk=userId)

class addStudentGivingLessons(forms.Form):
    givingLessons       = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                       queryset =None)
    addUser                = forms.IntegerField()
    
    def __init__(self, userId, *args, **kwargs):
        super(addStudentGivingLessons, self).__init__(*args, **kwargs)
        self.fields['givingLessons'].queryset = Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(person_ID = userId).values('fach_ID')))
        self.fields['addUser'].initial = userId

#Create Nachhilfe nehmen Form
class TakeNachhilfeForm(forms.ModelForm):
    class Meta:
        model = Teilnahme
        fields = '__all__'
        
class editStudentGivingLessons(forms.Form):
    editGivingLessons   = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, 
                                                        queryset=None)
    user                = forms.IntegerField()

    def __init__(self, userId, *args, **kwargs):
        super(editStudentGivingLessons, self).__init__(*args, **kwargs)
        self.fields['editGivingLessons'].queryset = Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(person_ID = userId).values('fach_ID')))
        self.fields['editGivingLessons'].initial = Faecher.objects.filter(pk__in=(Personen_Faecher.objects.filter(Q(person_ID = userId)& Q(nachhilfeflag=True)).values('fach_ID')))
        self.fields['user'].initial = userId


class messageInput(forms.ModelForm):
    class Meta:
        model = Sender
        fields = ('message', 'time', 'person_ID', 'empfaenger_ID')

    message = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(messageInput, self).__init__(*args, **kwargs)
        self.fields['message'].label =  False

class editUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    klasse = forms.CharField(max_length=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['last_name'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['email'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['klasse'].widget.attrs.update({'class': formsStyle["field"]})

        
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.PasswordInput()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class Settings_Content_Form(forms.ModelForm):
    class Meta:
        model = Settings_Content
        fields = ('impressum', 'datenschutz')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['impressum'] = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":20}))
        self.fields['impressum'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['datenschutz'] = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":20}))
        self.fields['datenschutz'].widget.attrs.update({'class': formsStyle["field"]})
        self.fields['impressum'].inital = Settings_Content.objects.get(id=1).impressum
        self.fields['datenschutz'].inital = Settings_Content.objects.get(id=1).datenschutz

class TeilnahmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teilnahme
        fields = '__all__'

class NachhilfeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nachhilfe
        fields = '__all__'