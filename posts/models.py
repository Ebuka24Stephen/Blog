from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    like = models.ManyToManyField(User, related_name='likes',  blank=True)
    
    def total_likes (self):
        return self.like.count()
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented on {self.post.id} "
    
    def total_comment(self):
        return self.comment.count()