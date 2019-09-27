# Generated by Django 2.2.5 on 2019-09-26 22:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_shipper_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='biography',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: +9999999999. Up to 20 digits allowed.', regex='\\+?1?\\d{9, 20}$')]),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/pictures', verbose_name='Profile Image'),
        ),
        migrations.AddField(
            model_name='user',
            name='reputation',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='verified_id',
            field=models.BooleanField(default=False, help_text="Set to true when the user's ID is verified", verbose_name='Verified Identification'),
        ),
    ]