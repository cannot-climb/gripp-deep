# Generated by Django 4.1.1 on 2022-09-16 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("kilterboard", "0002_alter_climbvideo_upload_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="climbvideo",
            name="upload_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
