import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Create simple Question model"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Inform if the question was published recently"""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    """Create choice model related to Question model"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
