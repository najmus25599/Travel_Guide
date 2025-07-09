from django.db import models
from django.conf import settings

# Create your models here.



class Blog(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    category_choice = [('mountain', 'Mountain'), ('sea', 'Sea'), ('urban', 'Urban'), ('urban', 'Urban')]
    flair = models.CharField(max_length=120, choices=category_choice)
    title = models.CharField(max_length=250,blank=False)
    blog_img = models.ImageField(upload_to='bus/static/', blank=True, null=True)
    body = models.TextField(null=True,blank=True)
    object: models.Manager()

    def __str__(self):
        return self.title


class Upvote(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=False)
    object: models.Manager()

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=False)
    body = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    object: models.Manager()