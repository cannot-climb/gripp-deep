from django.contrib import admin

from .models import ClimbVideo


class ClimbVideoAdmin(admin.ModelAdmin):
    fields = ["video_url", "video", "title", "difficulty", "degree", "upload_at"]
    list_display = ("title", "video", "video_url", "difficulty", "degree", "upload_at")


admin.site.register(ClimbVideo, ClimbVideoAdmin)
# Register your models here.
