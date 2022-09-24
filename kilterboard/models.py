from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class ClimbVideo(models.Model):
    video_url = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    degree = models.IntegerField(
        validators=[MaxValueValidator(70), MinValueValidator(0)]
    )
    difficulty = models.IntegerField(
        validators=[MaxValueValidator(19), MinValueValidator(0)]
    )
    upload_at = models.DateTimeField(default=timezone.now)

    video = models.FileField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    success = models.BooleanField(default=False)


# Create your models here.
