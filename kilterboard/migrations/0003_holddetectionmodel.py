# Generated by Django 4.1.2 on 2022-10-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "kilterboard",
            "0002_alter_climbvideo_degree_alter_climbvideo_difficulty_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="HoldDetectionModel",
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
                ("model_path", models.CharField(max_length=255)),
                ("score", models.FloatField()),
                ("wandb_artifact_path", models.CharField(max_length=255)),
                ("wandb_log_path", models.CharField(max_length=255)),
            ],
        ),
    ]
