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

    video = models.FileField(blank=True)
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    success = models.BooleanField(blank=True)


# Create your models here.
