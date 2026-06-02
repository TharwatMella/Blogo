import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django.setup()

from basic_app.models import Post


class A:
    def printme(self):
        print("I am in the Class A")

    def caller(self):
        self.printme()


class B(A):
    def printme(self):
        print("I am in Class B")


B().caller()
