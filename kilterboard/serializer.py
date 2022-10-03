from rest_framework import serializers

from .models import ClimbVideo


class ClimbVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbVideo
        fields = ("video_url", "title", "degree", "difficulty")


class ResponseClimbVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbVideo
        fields = ("title", "video_url", "start_time", "end_time", "success")
