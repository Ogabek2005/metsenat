# Generated by Django 5.0.3 on 2024-03-20 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_rename_amount_sponsor_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.university', verbose_name='University'),
        ),
    ]
