# Generated by Django 4.1 on 2022-11-19 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='day1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='day2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='day3',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='day4',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='day5',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='level',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='points',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='productivity_percentage',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='streak',
        ),
        migrations.AlterField(
            model_name='profile',
            name='code',
            field=models.CharField(default='YGMZNCDR', max_length=10),
        ),
    ]
