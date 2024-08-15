from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank= True)    

    def __str__(self) -> str:
        return self.title
    
    