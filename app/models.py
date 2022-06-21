from random import random, randint

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from coolname import generate_slug
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

TITLE_LENGTH = 1024
CONTENT_LENGTH = 65536
TAG_LENGTH = 128

NUMBER_OF_USERS = 2
NUMBER_OF_QUESTIONS = 200
NUMBER_OF_ANSWERS = 2000
NUMBER_OF_TAGS = 20


class Tag(models.Model):
    title = models.CharField(max_length=64, verbose_name="Tag")

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='panda.png', upload_to='avatar/%Y/%m/%d/')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username



class AnswerManager(models.Manager):
    def get_answer_by_question(self, question_id: int):
        return self.filter(question_id=question_id)


class Answer(models.Model):
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE, default=1)
    author = models.OneToOneField('Profile', related_name='answers', on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    user_rating = models.IntegerField(null=True)

    objects = AnswerManager()


class Like(models.Model):
    user = models.ForeignKey(Profile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    question = models.ForeignKey('Question', related_name='likes', on_delete=models.CASCADE, default=0, blank=True, null=True)
    answer = models.ForeignKey(Answer, related_name='likes', on_delete=models.CASCADE, default=0, blank=True,
                                 null=True)

    object_id = models.PositiveIntegerField()
    like_object = GenericForeignKey('content_type', 'object_id')


class QuestionManager(models.Manager):
    def get_popular(self):
        return self.filter(likes__gt=10)

    def get_recent(self):
        return self.filter(published_date__gt=now())

    def get_question_by_id(self, question_id):
        return self.filter(id=question_id)

    def get_questions_by_user_id(self, user_id):
        return self.filter(author__user=user_id)

    def get_questions_by_tag_title(self, title):
        return self.filter(tags__title=title)

    def get_question_answers(self, question_id: int):
        return self.filter(author__answers__question_id=question_id)


class Question(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH, blank=False)
    content = models.CharField(max_length=CONTENT_LENGTH, blank=False)
    author = models.ForeignKey(Profile, related_name='questions', on_delete=models.CASCADE, default=1)
    published_date = models.DateTimeField(blank=True, auto_now=True)
    number_of_answers = models.IntegerField(null=True, default=0)
    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_question_answer(self):
        return self.answers