from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.utils import timezone


class ClimbVideo(models.Model):
    video_url = models.CharField(max_length=255)
    title = models.CharField(max_length=100, null=True, blank=True)
    degree = models.IntegerField(
        validators=[MaxValueValidator(70), MinValueValidator(0)], null=True, blank=True
    )
    difficulty = models.IntegerField(
        validators=[MaxValueValidator(19), MinValueValidator(0)], null=True, blank=True
    )
    upload_at = models.DateTimeField(default=timezone.now)

    video = models.FileField(
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["avi", "mp4", "mov"])],
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    success = models.BooleanField(default=False)


# Create your models here.
