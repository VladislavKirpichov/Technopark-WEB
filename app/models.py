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
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    author = models.OneToOneField('Profile', related_name='answers', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return self.content

    def likes(self):
        return LikeAnswer.objects.filter(answer_id=self.id).count()

    def like(self, profile):
        like = LikeAnswer.objects.filter(answer_id=self.id, profile=profile)
        if like:
            like.delete()
        else:
            like = LikeAnswer(answer_id=self.id, profile=profile)
            like.save()

    def set_correct_answer(self):
        self.is_correct = True
        self.save()

    def set_not_correct_answer(self):
        self.is_correct = False
        self.save()


class QuestionManager(models.Manager):
    def all(self):
        return self.order_by('published_date')

    def hot(self):
        return self.order_by('likes')

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
    author = models.ForeignKey(Profile, related_name='questions', on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_question_answer(self):
        return self.answers

    def likes(self):
        return LikeQuestion.objects.filter(question_id=self.id).count()

    def like(self, profile: Profile):
        like = LikeQuestion.objects.filter(question_id=self.id, profile=profile)
        if like:
            like.delete()
        else:
            like = LikeQuestion(question_id=self.id, profile=profile)
            like.save()

    def number_of_answers(self):
        return Answer.objects.filter(question_id=self.id).count()

    def get_author_username(self):
        return self.author.user.username


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, related_name="like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tests = models.CharField(default="test", max_length=123)

    def __str__(self):
        return f"{self.profile.user.username} {self.question.title}"


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name="like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.answer.question.title}"
