from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    # slow query
    for p in PeopleAddress.objects.all():
        print(p.people.name)

    #  fast query
    for p in PeopleAddress.objects.all().select_related('people')[0:10]:
        print(p.people.name)