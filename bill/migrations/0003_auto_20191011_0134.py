# Generated by Django 2.2.5 on 2019-10-11 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_bill_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bill', to='order.Order'),
        ),
    ]
