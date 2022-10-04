# Generated by Django 4.1.1 on 2022-10-04 13:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kilterboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="climbvideo",
            name="degree",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(70),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="climbvideo",
            name="difficulty",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(19),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="climbvideo",
            name="title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]