import time

import cv2
import mediapipe as mp
import math

import numpy as np
import torch
import errno
import os
import sys
import warnings
from typing import Optional
from urllib.parse import urlparse

from torch.hub import get_dir, HASH_REGEX, download_url_to_file

_model_param_url = {
    "yolov5n": "https://github.com/wonbeomjang/parameters/releases/download/parameter/yolov5n.pt",
    "yolov5n6": "https://github.com/wonbeomjang/parameters/releases/download/parameter/yolov5n6.pt",
}


def _load_param_str_from_url(
    url: str,
    model_dir: Optional[str] = None,
    progress: bool = True,
    check_hash: bool = False,
    file_name: Optional[str] = None,
) -> str:
    # Issue warning to move data if old env is set
    if os.getenv("TORCH_MODEL_ZOO"):
        warnings.warn(
            "TORCH_MODEL_ZOO is deprecated, please use env TORCH_HOME instead"
        )

    if model_dir is None:
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, "checkpoints")

    try:
        os.makedirs(model_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists, ignore.
            pass
        else:
            # Unexpected OSError, re-raise.
            raise

    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    if file_name is not None:
        filename = file_name
    cached_file = os.path.join(model_dir, filename)
    if not os.path.exists(cached_file):
        sys.stderr.write('Downloading: "{}" to {}\n'.format(url, cached_file))
        hash_prefix = None
        if check_hash:
            r = HASH_REGEX.search(filename)  # r is Optional[Match[str]]
            hash_prefix = r.group(1) if r else None
        download_url_to_file(url, cached_file, hash_prefix, progress=progress)

    return cached_file


class PoseDetector:
    def __init__(
        self,
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode,
            model_complexity,
            smooth_landmarks,
            enable_segmentation,
            smooth_segmentation,
            min_detection_confidence,
            min_tracking_confidence,
        )
        self.right_hand = {16, 18, 20, 22}
        self.left_hand = {15, 17, 19, 21}

    def __call__(self, img, factor=1.5):
        return self.make_hand_mask(img, factor)

    def make_hand_mask(self, img, factor=1.0):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        right_hand = {"x": [], "y": []}
        left_hand = {"x": [], "y": []}

        img = np.zeros(img.shape, np.uint8)
        if results.pose_landmarks:
            for i, lm in enumerate(results.pose_landmarks.landmark):
                if i in self.right_hand:
                    h, w, c = img.shape
                    right_hand["x"] += [int(lm.x * w)]
                    right_hand["y"] += [int(lm.y * h)]

                elif i in self.left_hand:
                    h, w, c = img.shape
                    left_hand["x"] += [int(lm.x * w)]
                    left_hand["y"] += [int(lm.y * h)]

        if right_hand["x"]:
            cx = sum(right_hand["x"]) // len(right_hand["x"])
            cy = sum(right_hand["y"]) // len(right_hand["y"])
            radius = 0
            for x, y in zip(right_hand["x"], right_hand["y"]):
                radius = max(radius, (cx - x) ** 2 + (cy - y) ** 2)
            img = cv2.circle(
                img, (cx, cy), int(math.sqrt(radius) * factor), (255, 255, 255), -1
            )

        if left_hand["x"]:
            cx = sum(left_hand["x"]) // len(left_hand["x"])
            cy = sum(left_hand["y"]) // len(left_hand["y"])
            radius = 0
            for x, y in zip(left_hand["x"], left_hand["y"]):
                radius = max(radius, (cx - x) ** 2 + (cy - y) ** 2)
            img = cv2.circle(
                img, (cx, cy), int(math.sqrt(radius) * factor), (255, 255, 255), -1
            )

        return img


class HoldDetector:
    def __init__(self, model_name: str = "yolov5n6"):
        path = _load_param_str_from_url(_model_param_url[model_name])
        self.net = torch.hub.load(
            "ultralytics/yolov5", "custom", path=path, verbose=False
        )
        self.name = {0: "foot", 1: "hand", 2: "start", 3: "top"}

    def __call__(self, img):
        df = self.net(img)
        size_t = df.ims[0].shape

        start_image = np.zeros(size_t, np.uint8)
        top_image = np.zeros(size_t, np.uint8)
        pred = df.pred[0]

        for p in pred:
            if p[-1] == 2.0:
                cv2.rectangle(
                    start_image,
                    (int(p[0]), int(p[1])),
                    (int(p[2]), int(p[3])),
                    (255, 255, 255),
                    -1,
                )
            if p[-1] == 3.0:
                cv2.rectangle(
                    top_image,
                    (int(p[0]), int(p[1])),
                    (int(p[2]), int(p[3])),
                    (255, 255, 255),
                    -1,
                )

        return start_image, top_image


def get_hold_mask(video_path, num_extract_frame=5):
    hold_detector = HoldDetector()

    cap = cv2.VideoCapture(video_path)
    num_interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_extract_frame
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    index = 0
    start_hold_mask = np.zeros((h, w, 3), np.uint8)
    top_hold_mask = np.zeros((h, w, 3), np.uint8)

    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        index += 1
        if index % num_interval != 0:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start_hold, top_hold = hold_detector(image)
        start_hold_mask = cv2.bitwise_or(start_hold_mask, start_hold)
        top_hold_mask = cv2.bitwise_or(top_hold_mask, top_hold)
    cap.release()

    return start_hold_mask, top_hold_mask


def get_video_result(video_path, start_hold_mask, top_hold_mask):
    pose_detector = PoseDetector()
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    start_frame = 0
    end_frame = length
    success = False

    index = 0
    while cap.isOpened():
        ret, image = cap.read()
        index += 1
        if not ret:
            break
        if index % fps != 0:
            continue

        hand = pose_detector(image, 2)

        if not start_frame and cv2.bitwise_and(start_hold_mask, hand).any():
            start_frame = index

        elif cv2.bitwise_and(top_hold_mask, hand).any():
            end_frame = index
            success = True
    cap.release()

    if start_frame == end_frame:
        end_frame += fps

    return start_frame / fps, end_frame / fps, success


if __name__ == "__main__":
    import datetime

    cur = time.time()
    video_path = "../media/test.mp4"

    start_hold_mask, top_hold_mask = get_hold_mask(video_path)
    start_second, end_second, success = get_video_result(
        video_path, start_hold_mask, top_hold_mask
    )
    start_second_int = int(start_second)
    end_second_int = int(end_second)
    start = datetime.time(
        start_second_int // 3600,
        (start_second_int % 3600) // 60,
        start_second_int % 60,
        microsecond=int((start_second - start_second_int) * 1000),
    )
    end = datetime.time(
        end_second_int // 3600,
        (end_second_int % 3600) // 60,
        end_second_int % 60,
        microsecond=int((end_second - end_second_int) * 1000),
    )
    print(time.time() - cur, start, end, success)
