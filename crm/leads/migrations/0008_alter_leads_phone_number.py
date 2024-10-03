# Generated by Django 5.1.1 on 2024-10-01 12:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_alter_leads_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leads',
            name='phone_number',
            field=models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: +7(921)6543210. Допустимо до 14 цифр.', regex='^\\+7[(]\\d{3}[)]\\d{7}$')], verbose_name='Номер телефона'),
        ),
    ]
