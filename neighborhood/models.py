from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from cloudinary.models import CloudinaryField 

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = CloudinaryField('gallery/',default='default.jpeg')
    bio = models.CharField(max_length=500)
    name = models.CharField(blank=True, max_length=120)
    neighborhood = models.ForeignKey('Neighborhood', on_delete=models.CASCADE, related_name='profile',null=True,blank=True)
    location = models.CharField(blank=True, max_length=120)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def __str__(self):
        return self.name

class Neighborhood(models.Model):
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(blank=True, max_length=120)
    admin = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='hood')
    hood_logo = CloudinaryField('gallery/')
    occupants_count = models.PositiveIntegerField(default = '0')
    description = models.TextField()
    health_department = models.IntegerField(null=True, blank=True)
    police_number = models.IntegerField(null=True, blank=True) 

    @classmethod
    def find_neighborhood(cls, neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)

    def save_post(self):
        self.save()

    @classmethod
    def update_post(cls,old,new):
        cap = Neighborhood.objects.filter(description=old).update(description=new)
        return cap

    def delete_post(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()

    def __str__(self):
        return f'{self.name} hood'

class Business(models.Model):
    name = models.CharField(max_length=120)
    photo = CloudinaryField('gallery/',default='default.jpeg',null=True)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    neighborhood = models.ForeignKey('NeighborHood', on_delete=models.CASCADE, related_name='business',null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner',null=True)

    def __str__(self):
        return f'{self.name} Business'

    @classmethod
    def find_business(cls, business_id):
        return cls.objects.filter(id=business_id)

    @classmethod
    def update_post(cls,old,new):
        cap = Business.objects.filter(description=old).update(description=new)
        return cap

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()

class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey('NeighborHood', on_delete=models.CASCADE, related_name='hood_post')
