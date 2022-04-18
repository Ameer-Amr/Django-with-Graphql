from django.db import models

# Create your models here.


class Director(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Movie(models.Model):
    title = models.CharField(max_length=32)
    year = models.IntegerField(default=2000)
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.title
