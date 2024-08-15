# Generated by Django 5.0.7 on 2024-07-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_checkout_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='address',
        ),
        migrations.AddField(
            model_name='checkout',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='district',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='number_house',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='street',
            field=models.CharField(max_length=255, null=True),
        ),
    ]