# Generated by Django 3.0.5 on 2020-05-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0011_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(default=' '),
        ),
    ]