# Generated by Django 5.1.3 on 2025-01-15 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_doctordetails_doctor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('doctor', 'Doctor')], default='user', max_length=15),
        ),
    ]
