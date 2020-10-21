from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follower(models.Model):

    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete= models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return str(self.following.id) 
    

class Post(models.Model):
    content = models.TextField(max_length=1000)
    create_date = models.DateTimeField( auto_now=True)
    creator = models.ForeignKey(User, on_delete= models.CASCADE, related_name='post_creator')
    likes = models.ManyToManyField("User", related_name='user_likes', blank=True)

    def total_likes(self):
        try:
            return self.likes.all().count()
        except:
            return None

    def short(self):
        return {
            "pk": self.id,
            "content": self.content,
            "creator_id": self.creator.id,
            "creator": self.creator.username,
            "create_date": self.create_date.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.id for user in self.likes.all()],
            "total_likes": self.total_likes()
        }