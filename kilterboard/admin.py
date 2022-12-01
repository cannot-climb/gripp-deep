from django.contrib import admin

from .models import ClimbVideo, HoldDetectionModel


class ClimbVideoAdmin(admin.ModelAdmin):
    fields = ["video_url", "video", "title", "difficulty", "degree", "upload_at"]
    list_display = ("title", "video", "video_url", "difficulty", "degree", "upload_at")


class HoldDetectionModelAdmin(admin.ModelAdmin):
    fields = ["wandb_artifact_path", "wandb_log_path"]
    list_display = (
        "id",
        "model_path",
        "score",
        "wandb_artifact_path",
        "wandb_log_path",
    )


admin.site.register(ClimbVideo, ClimbVideoAdmin)
admin.site.register(HoldDetectionModel, HoldDetectionModelAdmin)
# Register your models here.
