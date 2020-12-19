from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models.fields import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    image = ProcessedImageField(default="default.png", upload_to='profile_image', processors=[ResizeToFill(200, 200)],
                                format='JPEG', options={'quality': 90})
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(50, 50)], format='JPEG',
                               options={'quality': 100})

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'], id=kwargs['instance'].id)


post_save.connect(create_profile, sender=User)


class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='issue_images', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
