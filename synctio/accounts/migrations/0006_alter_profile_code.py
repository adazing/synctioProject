# Generated by Django 4.1 on 2022-10-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='code',
            field=models.CharField(default='KCPUBOBW', max_length=10),
        ),
    ]