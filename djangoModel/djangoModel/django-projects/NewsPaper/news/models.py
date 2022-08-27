from django.db import models
from django.contrib.auth.models import User
from

news = 'NE'
article = 'AR'

TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
    ]
# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, default=0, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)


    def update_rating(userid):
    #    Author.objects.filter(id=userid, Post.kind="")
    #    Author.objects.filter(age__lt=25)
    a = Author()
    pass


class Category(models.Model):  # наследуемся от класса Model
    name = models.CharField(max_length = 128, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    kind = models.CharField(max_length=255, choices=TYPES)
    creation_date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.text[::124] + "..."

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

