# Generated by Django 4.1.7 on 2023-04-24 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("branches", "0002_alter_branch_options"),
        ("rooms", "0012_remove_room_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="brand",
        ),
        migrations.AddField(
            model_name="room",
            name="branch",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="branches.branch",
            ),
            preserve_default=False,
        ),
    ]
