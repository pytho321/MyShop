# Generated by Django 4.1.5 on 2023-02-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mainApp",
            "0003_alter_seller_addressline1_alter_seller_addressline2_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(model_name="seller", name="pincode",),
        migrations.AddField(
            model_name="seller",
            name="addressline3",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="seller",
            name="pin",
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="addressline1",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="addressline2",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="seller",
            name="email",
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="seller", name="name", field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="seller",
            name="username",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]