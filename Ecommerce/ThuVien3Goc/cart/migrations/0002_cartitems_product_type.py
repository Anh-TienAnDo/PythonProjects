# Generated by Django 5.0.6 on 2024-07-13 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='product_type',
            field=models.CharField(default='USB', max_length=20),
        ),
    ]