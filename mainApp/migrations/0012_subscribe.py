# Generated by Django 4.1.5 on 2023-04-08 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0011_checkout_active_alter_checkout_mode"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscribe",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=50)),
            ],
        ),
    ]
