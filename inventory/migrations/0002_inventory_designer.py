# Generated by Django 2.2.5 on 2019-10-01 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='designer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='users.Designer'),
        ),
    ]
