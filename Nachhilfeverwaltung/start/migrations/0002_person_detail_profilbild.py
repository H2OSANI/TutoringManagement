# Generated by Django 4.1.2 on 2022-11-06 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person_detail',
            name='profilBild',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
