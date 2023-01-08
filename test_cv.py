import os

import cv2
from unittest import TestCase
from urllib import request

from kilterboard.cv import get_hold_mask, get_video_result


def get_result(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    hand_hold_mask, start_hold_mask, top_hold_mask = get_hold_mask(video_path)
    start_second, end_second, success = get_video_result(
        video_path, hand_hold_mask, start_hold_mask, top_hold_mask
    )
    return start_second, end_second, success, duration


class ComputerVisionModuleTest(TestCase):
    fail_video_url = "https://github.com/cannot-climb/gripp-deep/releases/download/parameter/fail.mp4"
    success_video_url = "https://github.com/cannot-climb/gripp-deep/releases/download/parameter/success.mp4"
    fail_video_path = "fail.MOV"
    success_video_path = "success.MOV"

    @classmethod
    def setUp(cls):
        request.urlretrieve(cls.fail_video_url, cls.fail_video_path)
        request.urlretrieve(cls.success_video_url, cls.success_video_path)

    def test_video_result(self):
        start_second, end_second, success, duration = get_result(
            self.success_video_path
        )
        self.assertTrue(0 <= start_second <= end_second <= duration)
        self.assertTrue(success)

        start_second, end_second, success, duration = get_result(self.fail_video_path)
        self.assertTrue(0 <= start_second <= end_second <= duration)
        self.assertFalse(success)

    @classmethod
    def tearDown(cls):
        os.remove(cls.fail_video_path)
        os.remove(cls.success_video_path)
