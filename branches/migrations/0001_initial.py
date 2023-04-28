# Generated by Django 4.1.7 on 2023-04-03 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("brands", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=140)),
                ("location", models.CharField(max_length=1000)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="brands.brand"
                    ),
                ),
            ],
        ),
    ]