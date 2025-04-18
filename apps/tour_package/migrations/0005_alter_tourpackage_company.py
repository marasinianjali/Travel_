# Generated by Django 5.2 on 2025-04-10 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_package', '0004_remove_tourpackage_company_name_tourpackage_company_and_more'),
        ('tourism_company', '0003_tourismcompany_is_active_tourismcompany_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpackage',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourism_company.tourismcompany'),
        ),
    ]
