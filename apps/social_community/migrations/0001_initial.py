from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('user_login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=models.CASCADE, related_name='following', to='user_login.User')),
                ('followed', models.ForeignKey(on_delete=models.CASCADE, related_name='followed', to='user_login.User')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('follower', 'followed')},
                'db_table': 'follows',  # Matches your SQL
            },
        ),
    ]