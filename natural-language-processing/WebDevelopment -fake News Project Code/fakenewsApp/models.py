#from django.db import models

# Create your models here.
from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class fakenewsModel(models.Model):

    fakenews=models.CharField(max_length=5000)
