# Generated by Django 5.2 on 2025-04-22 07:37

import fernet_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_stories', '0003_alter_article_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=fernet_fields.fields.EncryptedTextField(help_text='Main content of the article.', verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=fernet_fields.fields.EncryptedDateTimeField(auto_now_add=True, help_text='Timestamp when the article was created.', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=fernet_fields.fields.EncryptedCharField(help_text='Title of the article.', max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated_at',
            field=fernet_fields.fields.EncryptedDateTimeField(auto_now=True, help_text='Timestamp when the article was last updated.', verbose_name='Updated At'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=fernet_fields.fields.EncryptedTextField(help_text='Content of the comment.', verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=fernet_fields.fields.EncryptedDateTimeField(auto_now_add=True, help_text='Timestamp when the comment was made.', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=fernet_fields.fields.EncryptedDateTimeField(auto_now_add=True, help_text='Timestamp when the like was made.', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='travelnews',
            name='content',
            field=fernet_fields.fields.EncryptedTextField(help_text='Content of the travel news.', verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='travelnews',
            name='created_at',
            field=fernet_fields.fields.EncryptedDateTimeField(auto_now_add=True, help_text='Timestamp when the news was published.', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='travelnews',
            name='title',
            field=fernet_fields.fields.EncryptedCharField(help_text='Title of the travel news.', max_length=200, verbose_name='Title'),
        ),
    ]
