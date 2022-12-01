from rest_framework import serializers

from .models import ClimbVideo, HoldDetectionModel


class ClimbVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbVideo
        fields = ("video_url",)


class ResponseClimbVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbVideo
        fields = ("video_url", "start_time", "end_time", "success")


class HoldDetectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoldDetectionModel
        fields = ("wandb_artifact_path", "wandb_log_path")
