from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=55, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=20, null=True)),
                ('status', models.CharField(choices=[('married', 'Married'), ('unmarried', 'Unmarried')], default='married', max_length=20)),
                ('dob', models.DateField()),
                ('bio', models.TextField(blank=True, null=True)),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark')], default='light', max_length=50)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]