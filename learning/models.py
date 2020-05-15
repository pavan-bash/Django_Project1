from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Domain(models.Model):
    name = models.CharField(max_length = 200, null=True)
    pic = models.ImageField(upload_to = 'profile_pics')
    desc = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    domain = models.ForeignKey(Domain, null=True, on_delete= models.CASCADE)
    name = models.CharField(max_length = 200, null=True)
    pic = models.ImageField(upload_to = 'profile_pics')
    desc = models.TextField()

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    coursename = models.ForeignKey(Course, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.coursename.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='Other')
    This_blog_is_about = models.CharField(max_length=400, default="This shows up in public blog! Choose well.")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    postname = models.ForeignKey(Post, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.postname.title

class PublicComment(models.Model):
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username.title

class Like(models.Model):
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    postname = models.ForeignKey(Post, null=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.postname.title 

