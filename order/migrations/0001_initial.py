# Generated by Django 2.2.5 on 2019-10-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was last modified', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified', verbose_name='modified at')),
                ('optional_address', models.CharField(default=None, max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'none'), (1, 'placed'), (2, 'shipped'), (3, 'on_the_way'), (4, 'arrived'), (5, 'missing')], default=0)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
