from audio.helper import get_audio_length
from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=20)
    artiste = models.CharField(max_length=500)
    artist_image = models.ImageField(upload_to='art/')
    time_length = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    audio_file = models.FileField(upload_to='musics/')
    cover_image = models.ImageField(upload_to='music_images/')

    def save(self, *args, **kwargs):
        if not self.time_length:
            # logic for getting length of audio
            audio_length = get_audio_length(self.audio_file)
            self.time_length = f'{audio_length:.2f}'

        return super().save(*args, **kwargs)

    class Meta:  # Corrected from META to Meta
        ordering = ("id",)  # Corrected from "id" to ("id",)

