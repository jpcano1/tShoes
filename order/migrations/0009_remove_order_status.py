# Generated by Django 2.2.5 on 2019-10-01 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20191001_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
