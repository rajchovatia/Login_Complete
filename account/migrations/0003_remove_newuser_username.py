# Generated by Django 4.2.7 on 2023-12-20 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_newuser_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='username',
        ),
    ]
