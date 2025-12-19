from django.db import models
from django.contrib.auth.models import User

# Create your models here. 

def chat_image_upload_path(instance,filename):
    return f'user_{instance.user.id}/chat/{filename}'

class Conversation(models.Model):
    user_1 = models.ForeignKey(User,related_name='sending_user', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User,related_name='reciving_user' ,on_delete=models.CASCADE) 
    last_sent = models.DateTimeField(auto_now=True)

    def get_last_message(self):
        return self.conversation_message.last()

class Message(models.Model):
   conversation = models.ForeignKey(Conversation,related_name='conversation_message', on_delete=models.CASCADE)
   sender = models.ForeignKey(User, on_delete=models.CASCADE)
   text = models.TextField(default='')
   image = models.ImageField(upload_to='chat_image_upload_path',blank=True,null=True)
   is_seen = models.BooleanField(default=False)
   edited = models.BooleanField(default=False)
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return f'{self.sender} sent message.seen={self.is_seen}'
       