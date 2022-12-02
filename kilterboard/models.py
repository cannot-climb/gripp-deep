import os
import datetime
import logging
import uuid

from django.conf import settings
from urllib import request
from urllib.parse import urlparse
from urllib.error import HTTPError

from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.utils import timezone

from kilterboard.cv import get_hold_mask, get_video_result

logger = logging.getLogger("gripp.settings")


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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        video_url = self.video_url
        base_name = self.get_unique_basename(urlparse(video_url).path)
        video_path = os.path.join(settings.MEDIA_ROOT, base_name)

        try:
            opener = request.build_opener()
            opener.addheaders = [
                ("Authorization", f"Basic {os.environ['GRIPP_BASIC_TOKEN']}")
            ]
            request.install_opener(opener)
        except KeyError:
            logger.error("os.environ['GRIPP_BASIC_TOKEN'] does not found")

        try:
            request.urlretrieve(video_url, video_path)
        except HTTPError as e:
            return e.status

        hand_hold_mask, start_hold_mask, top_hold_mask = get_hold_mask(video_path)
        start_second, end_second, success = get_video_result(
            video_path, hand_hold_mask, start_hold_mask, top_hold_mask
        )

        start_second_int = int(start_second)
        end_second_int = int(end_second)

        self.video = base_name
        self.start_time = datetime.time(
            start_second_int // 3600,
            (start_second_int % 3600) // 60,
            start_second_int % 60,
            int((start_second - start_second_int) * 1000 * 1000),
        )
        self.end_time = datetime.time(
            end_second_int // 3600,
            (end_second_int % 3600) // 60,
            end_second_int % 60,
            int((end_second - end_second_int) * 1000 * 1000),
        )
        self.success = success
        super().save(force_insert, force_update, using, update_fields)

    def get_unique_basename(self, path):
        base_name = os.path.basename(path)
        filename, extension = os.path.splitext(base_name)
        return filename + "-" + str(uuid.uuid4()).replace("-", "") + extension


# Create your models here.
