# Generated by Django 2.2.5 on 2019-09-27 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_bill_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
