from django.db import models


class Item(models.Model):
    hacker_news_id = models.PositiveIntegerField("HackerNews ID", unique=True)
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
