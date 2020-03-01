from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='question-detail')

    class Meta:
        model = models.Survey
        fields = ('url', 'pk', 'created', 'name', 'questions')


class QuestionSerializer(serializers.HyperlinkedRelatedField):
    owner = serializers.ReadOnlyField(read_only=True, source='owner.username')
    survey = serializers.SlugRelatedField(queryset=models.Survey.objects.all(), slug_field='name')

    class Meta:
        model = models.Question
        fields = ('url', 'owner', 'created', 'no', 'question_text', 'survey')


class ChoiceSerializer(serializers.HyperlinkedRelatedField):
    question = QuestionSerializer()

    class Meta:
        model = models.ParticipantChoice
        fields = ('url', 'question', 'choice')


class ParticipantSerializer(serializers.HyperlinkedRelatedField):
    gender = serializers.ChoiceField(choices=models.Participant.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Participant
        fields = ('url', 'name', 'gender', 'gender_description', 'choices')


class ParticipantChoiceSerializer(serializers.HyperlinkedRelatedField):
    question = serializers.SlugRelatedField(queryset=models.Question.objects.all(), slug_field='question_text')
    participant = serializers.SlugRelatedField(question=models.Participant.objects.all(), slug_field='name')

    class Meta:
        model = models.ParticipantChoice
        fields = ('url', 'question', 'participant', 'choice')


class UserQuestionSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = models.Question
        fields = ('url', 'no', 'question_text')


class UserSerializer(serializers.HyperlinkedRelatedField):
    questions = UserQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username', 'questions')