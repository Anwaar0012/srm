<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE)
=======
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE)
>>>>>>> origin/main
