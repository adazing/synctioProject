# Generated by Django 4.1 on 2022-10-10 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_code_alter_profile_lasttimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='code',
            field=models.CharField(default='YKDFMTXF', max_length=10),
        ),
    ]