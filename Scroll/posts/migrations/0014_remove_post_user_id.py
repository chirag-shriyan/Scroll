# Generated by Django 5.0.2 on 2024-02-28 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_post_post_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user_id',
        ),
    ]