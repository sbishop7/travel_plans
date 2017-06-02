# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect
from ..logreg.models import User
from .models import Trip
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'user_trips': Trip.objects.filter(travelers__id=request.session['user_id']),
            'other_trips': Trip.objects.all().exclude(travelers__id=request.session['user_id'])
        }
        return render(request, 'plans/index.html', context)
    else:
        return redirect( reverse( "logreg:index" ) ) 
    
def logout(request):
    del request.session['user_id']
    return redirect( "logreg:index" )

def add(request):
    if 'user_id' in request.session:
        return render(request, 'plans/add.html')
    else:
        return redirect( reverse( "logreg:index" ) ) 

def destination(request, id):
    if 'user_id' in request.session:
        context = {
            'trip': Trip.objects.get(id=id),
            'other_users': User.objects.filter(trips__id=id).exclude(id=request.session['user_id']).exclude(planning__id=id)
        }
        return render(request, 'plans/destination.html', context)
    else:
        return redirect( reverse( "logreg:index" ) ) 

def create(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            response_from_models = Trip.objects.add_trip(request.POST)
            if response_from_models['status']:
                return redirect('plans:index')
            else:
                for error in response_from_models['errors']:
                    messages.error(request, error)
                return redirect( reverse( "plans:add" ) ) 
    else:
        return redirect( reverse( "logreg:index" ) ) 

def join(request, id):
    if 'user_id' in request.session:
        Trip.objects.join(id, request.session['user_id'])
        return redirect( reverse('plans:index') ) 
    else:
        return redirect( reverse( "logreg:index" ) ) 