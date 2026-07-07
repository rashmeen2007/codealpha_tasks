from django.db import models

class User(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    joined_at = models.DateTimeField(auto_now_add=True)
class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )

    likes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    text = models.TextField()

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    message = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)