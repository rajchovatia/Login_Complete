# Generated by Django 5.0.1 on 2024-01-26 04:44

import account.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_newuser_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='newuser',
            managers=[
                ('objects', account.manager.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='newuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='user_bio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
