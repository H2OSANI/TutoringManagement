# Generated by Django 4.1.2 on 2022-11-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0004_alter_faecher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faecher',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
