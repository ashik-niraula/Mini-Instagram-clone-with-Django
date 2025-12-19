from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_delete,post_save
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import uuid
# Create your models here.
def post_upload_path(instance,filename):
    return f'user_{instance.user_id}/{filename}'

class Hagtag(models.Model):
    name = models.CharField(max_length=30) 
    created_at = models.DateField( auto_now_add=True)   

    def get_absolute_url(self):
        return reverse("hagtag_posts", kwargs={"hagtag": self.name})
    
    def __str__(self):
        return self.name
    
    
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    caption = models.TextField(max_length=2200,blank=True)

    image = models.ImageField(upload_to=post_upload_path,blank=False,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg' , 'png', 'gif'])]
                              )
    
    location = models.CharField( max_length=200,blank=True)

    hagtag = models.ManyToManyField(Hagtag,blank=True,related_name='post_hagtags')

    slug = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)

    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    def update_like_count(self):
        self.likes_count = self.post_likes.count()
        self.save(update_fields=['likes_count'])
    def update_comment_count(self):
        self.comment_count = self.post_comments.count()
        self.save(update_fields=['comment_count'])

    def extract_hagtags(self):
        import re
        if self.caption:
            found_hagtags = re.findall(r"#(\w+)",self.caption)
            for tag_name in found_hagtags:
                hagtag , created = Hagtag.objects.get_or_create(name=tag_name)
                self.hagtag.add(hagtag)


    class Meta:
        db_table = 'posts'
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.user.username}'s Post Uploaded at {self.posted_at.strftime('%Y-%m-%d')} "
    def get_absolute_url(self):
        return reverse("detail", kwargs={"post_id": self.id})
    
class Follow(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    following = models.ForeignKey(User, related_name='followers' , on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following' , on_delete=models.CASCADE)
    is_mutual = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['follower','following']


    

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
    
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} liked post"

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField(max_length=1000,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"    
    
class Saved_Post(models.Model):
        id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=True)
        user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_saving')
        post = models.ForeignKey(Post,on_delete=models.CASCADE)
        saved_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = ['user','post']

        def __str__(self):
            return f'{self.user.username} saved {self.post.id}'
        
        def get_absolute_url(self):
            return reverse('saved_posts')
        
class Seen_Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            unique_together = ['user','post']

    def __str__(self):
            return f'{self.user.username} seen {self.post.id}'
