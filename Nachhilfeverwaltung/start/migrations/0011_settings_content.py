# Generated by Django 4.1.2 on 2022-12-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0010_alter_sender_empfaenger_id_alter_sender_person_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings_Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impressum', models.CharField(max_length=10000)),
                ('datenschutz', models.CharField(max_length=10000)),
            ],
        ),
    ]