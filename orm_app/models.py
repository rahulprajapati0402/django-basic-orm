from django.db import models
import uuid

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

# This will not create model in database on migration
    class Meta:
        abstract = True


# BaseModel fields will be automatically added to this model.
class Colors(BaseModel):
    color_code = models.CharField(max_length=50)


# BaseModel fields will be automatically added to this model.
class People(BaseModel):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(max_length=254)
    colors = models.ManyToManyField(Colors)


# BaseModel fields will be automatically added to this model.
class PeopleAddress(BaseModel):
    """
    Using related_name, we can access address from People Model.
    For example,
        obj = People.objects.first()
        obj.address --> related_name
    """
    """
    on_delete=models.CASCADE - obj will be deleted on deleting parent obj
    on_delete=models.SET_NULL - obj will be set NULL on deleting parent obj
    on_delete=models.SET_DEFAULT - obj will be set default value on deleting parent obj
    """
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name="address")
    address = models.TextField()



# Django ORM - Object Relational Mapping - Part 1

obj = People.objects.all()
obj = People.objects.count()
obj = People.objects.filter(name = "Jhon")
obj = People.objects.filter(name__icontains = "Jh")
obj = People.objects.filter(name__icontains = "Jh", age = 21)
obj = People.objects.filter(name__icontains = "Jh")[0].name
obj = People.objects.filter(name__startswith = "Jon")
obj = People.objects.filter(name__endswith = "Jon")
obj = People.objects.filter(age = 21).count()
obj = People.objects.filter(age__gte = 18)      # greater than 18
obj = People.objects.filter(age__lte = 18)      # less than 18

PeopleAddress.objects.filter(people__name__icontains = "Jon")
PeopleAddress.objects.filter(people__email__icontains = "example.net").count()

obj = PeopleAddress.objects.first()
obj.address

obj = People.objects.first()
obj.name
obj.address    # related_name
obj.address.all()
obj.address.all().count()
obj.address.filter(address__icontains = "abc")

People.objects.get(age = 18)    # throw error when obj will none or more than one
People.objects.filter(age = 18)    # return all objs having age = 18

# will create obj if none | _ will return True if obj created or False if obj exists
obj, _ = People.objects.get_or_create(age = 1)

People.objects.all()[0:5]



# Django ORM - Object Relational Mapping - Part 2

People.objects.exclude(age = 21)    # will show all objs except age = 21
People.objects.exclude(age__gte = 21)    # will show all objs except age >= 21

People.objects.all().order_by('age')    # order by 1 --> 100
People.objects.all().order_by('name')    # order by A --> Z
People.objects.all().order_by('-age')    # order by 100 --> 1
People.objects.all().order_by('-name')    # order by Z --> A


from django.db.models import Count

People.objects.aggregate(Count('age'))
# --> {'age_count': 107}

from django.db.models import *

People.objects.aggregate(Sum('age'))
# --> {'age_sum': 3814}

People.objects.aggregate(Avg('age'))
# --> {'age_avg': 36.5444}

People.objects.aggregate(Min('age'))
# --> {'age_min': 1}

People.objects.aggregate(Max('age'))
# --> {'age_max': 50}

People.objects.filter(name__icontains = "John").aggregate(Max('age'))
# --> {'age_max': 47}

objs = People.objects.all().order_by('-age')[0:2]       # to find second largest age
objs[0].age     # --> 50
objs[1].age     # --> 49

from django.db.models import Q

# to filter people having age 29 or 30
People.objects.filter(Q(age = 30) | Q(age = 29))   # --> OR operator

# to update age by filtering
People.objects.filter(age = 30).update(age = 20)



# views.py