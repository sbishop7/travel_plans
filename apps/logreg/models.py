# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import bcrypt


class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append('Name is too short!')
        if len(postData['name']) == 0:
            errors.append('Name cannot be empty')
        if len(postData['username']) == 0:
            errors.append('Username cannot be empty')
        if len(postData['username']) < 3:
            errors.append('Userame is too short!')
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        if postData['password'] != postData['password_confirmation']:
            errors.append('Passwords must match')
        if self.filter(username = postData['username']):
            errors.append('Username is already registered')

        response_to_views = {}

        if errors:
            response_to_views['status'] = False
            response_to_views['errors'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = self.create(name = postData['name'], username = postData['username'], password = hashed_pw)
            response_to_views['status'] = True
            response_to_views['user'] = new_user

        return response_to_views


    def validate_login(self, postData):
        errors = []
        response_to_views = {}
        hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        try:
            user = self.get(username = postData['username'])
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password:
                response_to_views['status'] = True
                response_to_views['user'] = user
            else:
                errors.append('Username or Password does not match')
                response_to_views['status'] = False
                response_to_views['errors'] = errors
        except:
            errors.append('Username or Password does not match')
            response_to_views['status'] = False
            response_to_views['errors'] = errors

        return response_to_views


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()