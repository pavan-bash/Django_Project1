# Generated by Django 3.0.5 on 2020-05-13 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_auto_20200514_0438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='is_about',
            new_name='This_blog_is_about',
        ),
    ]
