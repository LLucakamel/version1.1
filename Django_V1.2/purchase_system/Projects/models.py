from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    consultant = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)

    def __str__(self):
        return self.name