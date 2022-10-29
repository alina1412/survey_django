from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.id} {self.title}"

    class Meta:
        db_table = "surveys"


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(blank=False)
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.id} {self.question[:14]}"

    class Meta:
        db_table = "questions"


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    choice = models.CharField(max_length=120)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.choice[:14]

    class Meta:
        db_table = "choices"


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.TextField(blank=True, null=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.answer[:14] if self.answer else ""

    class Meta:
        db_table = "answers"
