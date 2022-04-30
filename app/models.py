from random import random, randint

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from coolname import generate_slug
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

TITLE_LENGTH = 1024
CONTENT_LENGTH = 65536
TAG_LENGTH = 128

NUMBER_OF_USERS = 2
NUMBER_OF_QUESTIONS = 200
NUMBER_OF_ANSWERS = 2000
NUMBER_OF_TAGS = 20


class TagManager(models.Manager):
    def get_all(self):
        return self.all()

    def get_tag_by_name(self, name):
        return self.get(title=name)


class Tag(models.Model):
    title = models.CharField(max_length=64, verbose_name="Tag")
    questions = models.ManyToManyField('Question', related_name='tags')
    objects = TagManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images', null=True, blank=True,)
    bio = models.TextField(null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(Profile, related_name='answers', on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)
    user_rating = models.IntegerField(null=True)


class Like(models.Model):
    user = models.ForeignKey(Profile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    like_object = GenericForeignKey('content_type', 'object_id')

class QuestionManager(models.Manager):
    def get_tags(self, question_id: int):
        return Tag.objects.filter(question_id=question_id).all().values()

    def get_popular(self):
        return self.filter(likes__gt=10)

    def get_question_by_id(self, question_id):
        return self.filter(id=question_id)

    def get_questions_by_user_id(self, user_id):
        return Profile.objects.filter(id=user_id)

    def get_question_answers(self, question_id: int):
        return Answer.objects.filter(question_id=question_id)


class Question(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH, blank=True)
    content = models.CharField(max_length=CONTENT_LENGTH, blank=True)
    author = models.ForeignKey(Profile, related_name='questions', on_delete=models.CASCADE, default=1)
    published_date = models.DateTimeField(blank=True, auto_now=True)
    number_of_answers = models.IntegerField(null=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title
