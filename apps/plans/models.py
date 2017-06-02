# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User
import datetime

class TripManager(models.Manager):
    def add_trip(self, postData):
        errors = []
        response_to_views = {}
        today = str(datetime.date.today())

        user=User.objects.get(id=postData['user_id'])

        if len(postData['destination']) == 0:
            errors.append("Destination cannot be blank")
        if len(postData['description']) == 0:
            errors.append("Description cannot be blank")
        if len(postData['start']) == 0:
            errors.append("Travel Date From cannot be blank")
        if len(postData['end']) == 0:
            errors.append("Travel Date To cannot be blank")
        if str(postData['start']) < today:
            errors.append("Travel Date From cannot be in the past")
        if str(postData['end']) < str(postData['start']):
            errors.append('Travel Date To cannot be before Travel Date From')

        if errors:
            response_to_views['status'] = False
            response_to_views['errors'] = errors
        else: 
            response_to_views['status'] = True
            trip = self.create(destination=postData['destination'], description=postData['description'], start=postData['start'], end=postData['end'], planner=user)
            self.get( id = trip.id ).travelers.add( User.objects.get(id=postData['user_id']))

        return response_to_views
    
    def join(self, trip_id, user_id):
        self.get( id = trip_id ).travelers.add( User.objects.get( id = user_id ) )



class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    start = models.DateField(auto_now=False)
    end = models.DateField(auto_now=False)
    planner = models.ForeignKey(User, related_name="planning")
    travelers = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()