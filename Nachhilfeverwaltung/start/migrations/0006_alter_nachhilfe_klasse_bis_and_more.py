# Generated by Django 4.1.2 on 2022-11-16 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0005_alter_faecher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nachhilfe',
            name='klasse_bis',
            field=models.IntegerField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='nachhilfe',
            name='klasse_von',
            field=models.IntegerField(max_length=3, null=True),
        ),
    ]
