# Generated by Django 5.0.7 on 2024-07-31 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_checkout_address_checkout_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='product_slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]
