from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField()
    text = models.TextField()
    is_Published = models.BooleanField(default=False)
    creation_date = models.DateTimeField(
        default=timezone.now,
    )
    publication_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.publication_date = timezone.now()
        self.is_Published = True
        self.save()

    def __str__(self):
        return self.title + ": " + self.text

    def get_absolute_url(self):
        return reverse("blog:list")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def isBanned(self):
        if Blocklist.objects.get(post=self.post, user=self.user):
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.post.pk})

    def __str__(self):
        return self.text


class Blocklist(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + " & " + str(self.user) + " are in blocklist"
