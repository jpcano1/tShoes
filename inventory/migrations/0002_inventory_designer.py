<<<<<<< HEAD
# Generated by Django 2.2.6 on 2019-10-15 03:29
=======
# Generated by Django 2.2.5 on 2019-10-29 20:08
>>>>>>> security-develop

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='designer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='users.Designer'),
        ),
    ]
