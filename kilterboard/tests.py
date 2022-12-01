import datetime
from unittest import mock

import torch
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File

from .models import ClimbVideo, HoldDetectionModel


class KilterBoardTest(TestCase):
    url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
    title = "title"
    degree = 10
    difficulty = 1
    video = mock.MagicMock(spec=File)
    video.name = "test.mp4"
    start_time = datetime.time(minute=10, second=10)
    end_time = datetime.time(minute=20, second=10)
    success = True

    @classmethod
    def setUpTestData(cls):
        ClimbVideo.objects.create(
            video_url=cls.url,
            title=cls.title,
            degree=cls.degree,
            difficulty=cls.difficulty,
            video=cls.video,
            start_time=cls.start_time,
            end_time=cls.end_time,
            success=cls.success,
        )

    def test_create(self):
        instance1 = ClimbVideo(
            video_url=self.url, title=self.title, degree=90, difficulty=self.difficulty
        )
        instance2 = ClimbVideo(
            video_url=self.url, title=self.title, degree=self.degree, difficulty=-1
        )
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = "test.pdf"
        instance3 = ClimbVideo(
            video_url=self.url,
            title=self.title,
            degree=self.degree,
            difficulty=self.degree,
            video=file_mock,
        )
        instance4 = ClimbVideo(
            video_url=self.url,
            title=self.title,
            degree=self.degree,
            difficulty=self.degree,
            video=self.video,
        )

        self.assertRaises(ValidationError, instance1.full_clean)
        self.assertRaises(ValidationError, instance2.full_clean)
        self.assertRaises(ValidationError, instance3.full_clean)
        instance4.full_clean()

    def test_read(self):
        video = ClimbVideo.objects.get(title=self.title)
        self.assertEqual(self.url, video.video_url)
        self.assertEqual(self.title, video.title)
        self.assertEqual(self.degree, video.degree)
        self.assertEqual(self.difficulty, video.difficulty)


class HoldDetectionModelTest(TestCase):
    wandb_artifact_path = ("jtiger958/Gripp/run_1vl7goai_model:v0",)
    wandb_log_path = "jtiger958/Gripp/1vl7goai"

    def test_create(self):
        model = HoldDetectionModel.objects.create(
            wandb_artifact_path="jtiger958/Gripp/run_1vl7goai_model:v0",
            wandb_log_path="jtiger958/Gripp/1vl7goai",
        )

        torch.hub.load(
            "ultralytics/yolov5", "custom", path=model.model_path.path, verbose=False
        )
