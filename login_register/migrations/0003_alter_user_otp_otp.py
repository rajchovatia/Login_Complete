# Generated by Django 5.0.2 on 2024-02-16 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0002_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_otp',
            name='otp',
            field=models.IntegerField(),
        ),
    ]