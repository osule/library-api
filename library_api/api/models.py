# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Book(TimeStampMixin):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    category = models.CharField(max_length=200)


class Issue(TimeStampMixin):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    approved = models.BooleanField(default=False)
