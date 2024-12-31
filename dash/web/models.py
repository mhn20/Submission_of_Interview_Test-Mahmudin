from django.db import models


class Movie(models.Model):
    idxrow = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    imgPath = models.ImageField(upload_to='assets/images/')
    duration = models.IntegerField()
    genre = models.JSONField(blank=True, null=True)
    language = models.CharField(max_length=50)
    mpaaRating_type = models.CharField(max_length=10, blank=True, null=True)
    mpaaRating_label = models.CharField(max_length=255, blank=True, null=True)
    userRating = models.CharField(max_length=10)

    def __str__(self):
        return self.name
