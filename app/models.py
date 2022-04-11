from random import random, randint

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from coolname import generate_slug
from django.dispatch import receiver
from django.db.models.signals import post_save

TITLE_LENGTH = 1024
CONTENT_LENGTH = 65536
TAG_LENGTH = 128

NUMBER_OF_USERS = 2
NUMBER_OF_QUESTIONS = 200
NUMBER_OF_ANSWERS = 2000
NUMBER_OF_TAGS = 20

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempor id risus vel facilisis. Nunc " \
              "commodo non orci a mattis. Fusce nulla erat, mollis non ipsum ac, finibus accumsan ligula. Nam et " \
              "nulla eget neque consequat imperdiet. Ut pharetra odio aliquam lacinia lacinia. Curabitur non dui sed " \
              "est finibus tempor nec vitae dui. Donec fermentum leo arcu, nec finibus mi pretium nec. Proin finibus " \
              "semper purus vel convallis. Quisque eget fermentum dui. Morbi sollicitudin sit amet odio eget " \
              "dignissim. Curabitur nec nisi hendrerit neque rhoncus egestas at quis tellus. Pellentesque quam sem, " \
              "elementum eu sapien a, iaculis cursus lectus. Etiam ut nulla vel est ultricies fringilla. Maecenas " \
              "pretium ultricies nibh, efficitur cursus ante volutpat sit amet. "


# Create your models here.
class TagManager(models.Manager):
    def add_new_tags(self):
        tags = []
        for i in range(NUMBER_OF_TAGS):
            tags.append(Tag(tag=f"sample tag {i}"))

        self.bulk_create(tags)


class Tag(models.Model):
    tag = models.CharField(max_length=TAG_LENGTH, blank=True)
    objects = TagManager()


class ProfileManager(models.Manager):
    def add_new_profiles(self):
        profiles = []
        for i in range(NUMBER_OF_USERS):
            user = User.objects.create_user(
                username=generate_slug(4),
                email="sample@gmail.com",
                password=make_password("sample")
            )
            profiles.append(Profile(user=user, bio=LOREM_IPSUM))
            profiles[i].save()

        self.bulk_create(profiles)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images', null=True)
    bio = models.TextField(null=True)
    objects = ProfileManager()

class AnswerManager(models.Manager):
    def add_new_answers(self):
        answers = []
        for i in range(NUMBER_OF_ANSWERS):
            answers.append(Answer(author=User.objects.get(id=i % NUMBER_OF_USERS).id,
                                  question=Question.objects.get(id=i % NUMBER_OF_QUESTIONS).id,
                                  content=LOREM_IPSUM,
                                  user_rating=i % 10))

        self.bulk_create(answers)


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    user_rating = models.IntegerField(null=True)

    objects = AnswerManager()


class QuestionManager(models.Manager):
    def add_new_questions(self):
        questions = []
        for i in range(NUMBER_OF_QUESTIONS):
            questions.append(Question(tags=Tag.objects.all(),
                                      title=f"Sample Title {i}",
                                      content=LOREM_IPSUM,
                                      hot=(True if i % NUMBER_OF_TAGS == 0 else False),
                                      author=User.objects.get(id=i % NUMBER_OF_USERS),
                                      number_of_answers=10,
                                      # number_of_answers=len(Answer.objects.all().filter(author__question__in=self)),
                                      user_rating=100,
                                      ))

    def get_hot(self):
        return self.filter(hot=True)

    def get_popular(self):
        return self.filter(number_of_answers=10)

    def get_question_by_id(self, question_id):
        return self.filter(id=question_id)

    def get_questions_by_tag(self, tag: str):
        return self.filter(tags__in=tag)

    def get_question_answers(self, question_id: int):
        return Answer.objects.get(id in Question.answers)


class Question(models.Model):
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=TITLE_LENGTH, blank=True)
    content = models.CharField(max_length=CONTENT_LENGTH, blank=True)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE)
    hot = models.BooleanField()
    published_date = models.DateTimeField()
    author = models.ForeignKey(Profile, models.PROTECT)
    number_of_answers = models.IntegerField(null=True)
    user_rating = models.IntegerField(null=True)

    objects = QuestionManager()


