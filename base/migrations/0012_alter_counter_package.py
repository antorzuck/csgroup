# Generated by Django 5.0.6 on 2024-06-24 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_counter_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.fundpackage'),
        ),
    ]