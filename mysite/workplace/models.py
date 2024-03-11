from django.db import models


class Member(models.Model):
    discord_id = models.TextField()
    email = models.TextField()
    password = models.TextField()
    cookie = models.TextField()
