# Generated by Django 5.2 on 2025-04-10 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour_package', '0005_alter_tourpackage_company'),
        ('user_login', '0011_alter_booking_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='BookingDetail',
        ),
        migrations.AlterModelTable(
            name='bookingdetail',
            table='user_login_booking',
        ),
    ]
