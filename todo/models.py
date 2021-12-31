from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=300)
    desc = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

