from django.contrib import admin

from .models import ClimbVideo


class ClimbVideoAdmin(admin.ModelAdmin):
    fields = ["video", "title", "difficulty", "degree", "upload_at"]
    list_display = ("title", "video", "difficulty", "degree", "upload_at")


admin.site.register(ClimbVideo, ClimbVideoAdmin)
# Register your models here.
