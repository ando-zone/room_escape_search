# Generated by Django 4.1.7 on 2023-03-18 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0007_alter_room_difficulty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="difficulty",
            field=models.PositiveIntegerField(
                choices=[(1, "🔥"), (2, "🔥🔥"), (3, "🔥🔥🔥"), (4, "🔥🔥🔥🔥"), (5, "🔥🔥🔥🔥🔥")]
            ),
        ),
    ]