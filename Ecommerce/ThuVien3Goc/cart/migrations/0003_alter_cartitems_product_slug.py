# Generated by Django 5.0.6 on 2024-07-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitems_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='product_slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]
