# coding=utf-8

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_superuser(self, username, password, email=None, **extra_fields):

        if self.model.objects.filter(is_staff=True, is_superuser=True).exists():
            raise Exception("superuser is exist")

        user = self.model(username=username, email=email, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user
