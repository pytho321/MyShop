# Generated by Django 4.1.5 on 2023-04-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0012_subscribe"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactUs",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=50)),
                ("phone", models.CharField(max_length=15)),
                ("subject", models.CharField(max_length=20)),
                ("messages", models.CharField(max_length=20)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
    ]
