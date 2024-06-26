# Generated by Django 5.0.6 on 2024-06-26 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_profit_profits'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('method', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('number', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.profile')),
            ],
        ),
    ]
