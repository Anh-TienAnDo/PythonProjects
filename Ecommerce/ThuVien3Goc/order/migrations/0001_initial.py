# Generated by Django 5.0.6 on 2024-07-02 02:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('user_id', models.BigIntegerField(default=1)),
                ('person_name', models.CharField(max_length=255, null=True)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=12, null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('total', models.BigIntegerField(default=0)),
                ('status', models.CharField(choices=[('1', 'PENDING'), ('2', 'SHIPPED'), ('3', 'DELIVERED'), ('4', 'CANCELLED')], default='1', max_length=1)),
                ('date_order', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Checkouts',
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('product_slug', models.SlugField(null=True)),
                ('price', models.BigIntegerField(default=0)),
                ('quantity', models.IntegerField(blank=True, default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('checkout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.checkout')),
            ],
            options={
                'verbose_name_plural': 'OrderItems',
            },
        ),
    ]