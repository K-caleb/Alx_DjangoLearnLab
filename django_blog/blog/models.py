from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    """Model for a blog post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# NEW MODEL: Comment
class Comment(models.Model):
    """Model for a comment on a blog post."""
    # Link to the Post being commented on (many-to-one relationship)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    # Link to the User who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Content of the comment
    content = models.TextField()
    # Timestamp for creation
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for last update
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title[:20]}...'"
    
    def get_absolute_url(self):
        # After creating/editing a comment, redirect back to the post detail page
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    class Meta:
        # Order comments with the oldest first for a standard discussion flow
        ordering = ['created_at']
