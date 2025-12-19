from post.models import *
from django.db.models import Sum

# Create your models here.
def user_profile_image_upload_path(instance,filename):
    return f'user_{instance.user.id}/profile/{filename}'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_profile_image_upload_path,default='default-user.png')
    bio = models.CharField(max_length=120,blank=True,default='',null=True)
    location = models.CharField(max_length=80,blank=True,default='',null=True)
    website = models.URLField( max_length=200,blank=True,default='',null=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    total_likes_count = models.PositiveIntegerField(default=0)
    post_count = models.PositiveIntegerField(default=0)
    saved_post_count = models.PositiveIntegerField(default=0)

    def update_follower_count(self):
        self.follower_count = Follow.objects.filter(following=self.user).count()
        self.save(update_fields=['follower_count'])

    def update_following_count(self):
        self.following_count = Follow.objects.filter(follower=self.user).count()
        self.save(update_fields=['following_count'])

    def update_likes_count(self):
        total_likes = Post.objects.filter(user=self.user)\
        .aggregate(total_likes=Sum('likes_count'))['total_likes'] or 0
        
        self.total_likes_count =total_likes
        self.save(update_fields=['total_likes_count'])

    def update_post_count(self):
        self.post_count = Post.objects.filter(user=self.user).count()
        self.save(update_fields=['post_count'])
    
    def update_saved_post_count(self):
        self.saved_post_count = Saved_Post.objects.filter(user=self.user).count()
        self.save(update_fields=['saved_post_count'])

    def get_absolute_url(self):
        return reverse("profie-picture", kwargs={"id": self.id})
        

    def __str__(self):
        return self.user.username
        
    
    