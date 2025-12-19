from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from post.models import Like, Post, Follow,Saved_Post


@receiver([post_save,post_delete],sender=Like)
def update_profile_total_likes_count(sender,instance,**kwargs):
    instance.post.user.profile.update_likes_count()

@receiver([post_delete,post_save],sender=Post)    
def update_profile_total_post_count(sender,instance,**kwargs):
    instance.user.profile.update_post_count()

@receiver([post_save,post_delete],sender=Follow)    
def update_profile_follower_count(sender,instance,**kwargs):
    instance.following.profile.update_follower_count()


@receiver([post_delete,post_save],sender=Follow)
def update_profile_following_count(sender,instance,**kwargs):
    instance.follower.profile.update_following_count()  

@receiver([post_save,post_delete],sender=Saved_Post) 
def update_profile_saved_post_count(sender,instance,**kwargs):   
    instance.user.profile.update_saved_post_count()

