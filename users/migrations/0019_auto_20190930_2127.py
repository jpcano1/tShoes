# Generated by Django 2.2.5 on 2019-09-30 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20190929_1650'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='designer',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='shipper',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified']},
        ),
    ]
