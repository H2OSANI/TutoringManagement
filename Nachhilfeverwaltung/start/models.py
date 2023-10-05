from django.db import models
from django.contrib.auth.models import User

class Person_Detail(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   klasse = models.CharField(max_length=3, null=True)
   profilBild = models.ImageField(upload_to='media', null=True)


class Faecher(models.Model):
    fachbezeichnung = models.CharField(max_length=50, unique=True)

    def __str__(self):        
        return self.fachbezeichnung



class Nachhilfe(models.Model):
    preis = models.DecimalField(max_digits=10, decimal_places=2)
    klasse_von = models.IntegerField(null=True)
    klasse_bis = models.IntegerField(null=True)
    fach_ID = models.ForeignKey(Faecher, on_delete=models.CASCADE)
    person_ID = models.ForeignKey(User, on_delete=models.CASCADE)


class Teilnahme(models.Model):
    person_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    nachhilfe_ID = models.ForeignKey(Nachhilfe, on_delete=models.CASCADE)
    datum_uhrzeit = models.DateTimeField(null=True)
    

class Personen_Faecher(models.Model):
    person_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    fach_ID = models.ForeignKey(Faecher, on_delete=models.CASCADE)
    nachhilfeflag = models.BooleanField(default=0)

class Sender(models.Model):
    message = models.CharField(max_length=250)
    time = models.DateTimeField()
    person_ID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    empfaenger_ID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="empfaenger")
    newmessageflag = models.BooleanField(default=1)

class Settings_Content(models.Model):
    impressum = models.CharField(max_length=10000, null=True)
    datenschutz = models.CharField(max_length=10000, null=True)

    



