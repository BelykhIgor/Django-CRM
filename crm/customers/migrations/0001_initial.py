# Generated by Django 5.1.1 on 2024-09-19 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts', verbose_name='Контракт')),
                ('lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leads.leads', verbose_name='Потенциальный клиент')),
            ],
        ),
    ]
