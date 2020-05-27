# Generated by Django 2.2.12 on 2020-05-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('source', models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank')])),
                ('currency_type', models.PositiveSmallIntegerField(choices=[(1, 'USD'), (2, 'EUR'), (3, 'RUR')])),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Sale'), (2, 'Buy')])),
            ],
        ),
    ]
