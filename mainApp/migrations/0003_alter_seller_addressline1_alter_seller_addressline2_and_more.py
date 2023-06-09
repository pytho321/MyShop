# Generated by Django 4.1.5 on 2023-02-07 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0002_seller"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seller",
            name="addressline1",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="addressline2",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="city",
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="pincode",
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="state",
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
