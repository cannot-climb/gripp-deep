from rest_framework import serializers

from .models import ClimbVideo


class ClimbVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbVideo
        fields = ("video", "title", "degree", "difficulty")
