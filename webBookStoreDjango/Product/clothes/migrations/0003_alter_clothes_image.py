# Generated by Django 4.0.1 on 2024-03-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0002_producer_description_producer_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='image',
            field=models.TextField(),
        ),
    ]
