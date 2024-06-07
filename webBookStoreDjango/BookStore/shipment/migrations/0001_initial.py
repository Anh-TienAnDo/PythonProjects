# Generated by Django 4.0.1 on 2024-04-19 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout', models.BigIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=15, null=True)),
                ('shipper', models.CharField(max_length=255)),
                ('delivered', models.BooleanField(default=False)),
                ('date_shipment', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
