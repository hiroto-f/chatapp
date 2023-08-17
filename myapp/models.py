from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", 
        #img/uploads
        default="images/noimage.png"
    )

class Talk(models.Model):
    
    contents = models.CharField(max_length=200)
    talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talk_from')
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talk_to')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.talk_from
    


#password:summerintern(統一)
#superuser:hiroto
#user:kage,abe(abehiroshi)