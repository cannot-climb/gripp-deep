import os.path

import wandb
from django.conf import settings
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.utils import timezone


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


class HoldDetectionModel(models.Model):
    model_path = models.FileField()
    score = models.FloatField()

    wandb_artifact_path = models.CharField(max_length=255)
    wandb_log_path = models.CharField(max_length=255)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        artifact_dir, score = self.get_wandb_result(
            self.wandb_log_path, self.wandb_artifact_path
        )
        self.model_path = artifact_dir
        self.score = score

        super().save(force_insert, force_update, using, update_fields)

    def get_wandb_result(self, wandb_log_path, wandb_artifact_path):
        run = wandb.init(project="gripp-deep")
        artifact = run.use_artifact(wandb_artifact_path, type="model")
        run_id = wandb_log_path.split("/")[-1]
        artifact.download(root=os.path.join(settings.MEDIA_ROOT, run_id))
        run.finish()

        api = wandb.Api()
        # run is specified by <entity>/<project>/<run id>
        run = api.run(wandb_log_path)

        # save the metrics for the run to a csv file
        metrics_dataframe = run.history()

        metrics_dataframe["score"] = (
            metrics_dataframe["metrics/recall"] + metrics_dataframe["metrics/precision"]
        )
        score = metrics_dataframe["score"].max() / 2
        wandb.finish()

        artifact_path = os.path.join(run_id, "best.pt")

        return artifact_path, score


# Create your models here.
