# Generated by Django 4.1.5 on 2023-03-20 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0008_buyer_alter_seller_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mainApp.buyer"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainApp.product",
                    ),
                ),
            ],
        ),
    ]
