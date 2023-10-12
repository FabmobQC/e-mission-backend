#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import factory
from .models import User
from datetime import datetime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(
        lambda a: '{}@anonymous.com'.format(a.username).lower())
    date_joined = factory.LazyFunction(datetime.now)
    project = None
    server = None
    is_active = True
    is_staff = False
    is_superuser = False
