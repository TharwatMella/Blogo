import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django.setup()
from basic_app.models import Comment,Post

print(Comment.objects.first())