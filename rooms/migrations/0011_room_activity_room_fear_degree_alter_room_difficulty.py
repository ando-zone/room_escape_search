# Generated by Django 4.1.7 on 2023-04-03 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0010_alter_room_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="activity",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[(1, "🔑"), (2, "🔑🔑"), (3, "🔑🔑🔑"), (4, "🔑🔑🔑🔑"), (5, "🔑🔑🔑🔑🔑")],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="fear_degree",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[(1, "🔑"), (2, "🔑🔑"), (3, "🔑🔑🔑"), (4, "🔑🔑🔑🔑"), (5, "🔑🔑🔑🔑🔑")],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="difficulty",
            field=models.PositiveIntegerField(
                choices=[(1, "🔑"), (2, "🔑🔑"), (3, "🔑🔑🔑"), (4, "🔑🔑🔑🔑"), (5, "🔑🔑🔑🔑🔑")]
            ),
        ),
    ]
