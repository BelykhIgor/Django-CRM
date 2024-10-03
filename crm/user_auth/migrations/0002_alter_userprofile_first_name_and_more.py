# Generated by Django 5.1.1 on 2024-09-20 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Имя может содержать только русские или английские буквы.', regex='^[а-яА-ЯёЁa-zA-Z]+$')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Имя может содержать только русские или английские буквы.', regex='^[а-яА-ЯёЁa-zA-Z]+$')], verbose_name='Фамилия'),
        ),
    ]
