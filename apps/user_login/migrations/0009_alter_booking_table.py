# Generated by Django 5.2 on 2025-04-07 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0008_auto_20250402_0834'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='booking',
            table='user_login_booking',
        ),
    ]
