from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import *

@receiver([post_save,post_delete],sender=Like)
def update_post_likes_count(sender,instance,**kwargs):
    instance.post.update_like_count()

@receiver([post_save,post_delete],sender=Comment)
def update_post_comments_count(sender,instance,**kwargs)  :
    instance.post.update_comment_count()

@receiver(post_save,sender=Post) 
def extract_hagtags_from_caption(sender,instance,created,**kwargs):
    if created:
        instance.extract_hagtags()

@receiver(post_save,sender=Follow)
def update_mutual_follow(sender,instance,created,**kwargs):
    if created:
        if Follow.objects.filter(following=instance.follower,follower=instance.following):
            instance.is_mutual = True
            instance.save(update_fields=['is_mutual'])

            Follow.objects.filter(following=instance.follower,follower=instance.following).update(is_mutual=True)

@receiver(post_delete,sender=Follow)   
def update_mutual_on_unfollow(sender,instance,**kwargs)       :
    Follow.objects.filter(following=instance.follower,follower=instance.following).update(is_mutual=False)