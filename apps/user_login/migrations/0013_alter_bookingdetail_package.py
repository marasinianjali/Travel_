# Generated by Django 5.2 on 2025-04-15 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_package', '0007_alter_tourpackage_company'),
        ('user_login', '0012_rename_booking_bookingdetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetail',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_bookings', to='tour_package.tourpackage'),
        ),
    ]
