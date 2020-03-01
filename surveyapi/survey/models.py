from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Survey(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('-created', 'name', )

    def __str__(self):
        return self.name


class Question(models.Model):
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question_text = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    no = models.IntegerField()

    class Meta:
        ordering = ('no', )

    def __str__(self):
        return str(self.no) + ': ' + str(self.question_text)


class Participant(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class ParticipantChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, related_name='choices', on_delete=models.CASCADE)
    choice = models.IntegerField(default=-1)

    class Meta:
        ordering = ('participant', 'question', )
