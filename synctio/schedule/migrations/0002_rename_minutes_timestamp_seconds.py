# Generated by Django 4.1 on 2022-10-10 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timestamp',
            old_name='minutes',
            new_name='seconds',
        ),
    ]
