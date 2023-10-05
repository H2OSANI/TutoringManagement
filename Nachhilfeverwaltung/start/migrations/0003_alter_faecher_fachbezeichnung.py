# Generated by Django 4.1.2 on 2022-11-09 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0002_person_detail_profilbild'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faecher',
            name='fachbezeichnung',
            field=models.CharField(choices=[('DEUTSCH', 'Deutsch'), ('ENGLISCH', 'Englisch'), ('FRANZOESISCH', 'Franzoesisch'), ('LATEIN', 'Latein'), ('RUSSISCH', 'Russisch'), ('SPANISCH', 'Spanisch'), ('MATHEMATIK', 'Mathematik'), ('INFORMATIK', 'Informatik'), ('NATURWISSENSCHAFTEN', 'Naturwissenschaften'), ('TECHNIK', 'Technik'), ('GESELLSCHAFTSWISSENSCHAFTEN', 'Gesellschaftswissenschaften'), ('MUSIK', 'Musik'), ('SPORT', 'Sport'), ('BIOLOGIE', 'Biologie'), ('GESCHICHTE', 'Geschichte'), ('PHYSIK', 'Physik'), ('CHEMIE', 'Chemie'), ('ERDKUNDE', 'Erdkunde')], max_length=50, unique=True),
        ),
    ]