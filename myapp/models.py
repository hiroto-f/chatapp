from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Talk(models.Model):
    
    contents = models.CharField(max_length=200,verbose_name='')
    talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talk_from')
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talk_to')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.talk_from
    


#password:summerintern(統一)
#superuser:admin
#user:kage,abe