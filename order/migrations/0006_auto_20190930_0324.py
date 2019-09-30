# Generated by Django 2.2.5 on 2019-09-30 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20190929_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(0, 'none'), (1, 'placed'), (2, 'shipped'), (3, 'on_the_way'), (4, 'arrived'), (5, 'missing')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ManyToManyField(default=0, to='order.Status'),
        ),
    ]
