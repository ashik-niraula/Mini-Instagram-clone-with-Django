from .models import *
from django.db.models import When,Case,IntegerField
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def follow_suggestions(user):
    # Get people who follow me 
    follower_ids = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
    my_followers = User.objects.filter(id__in=follower_ids)
    
    # Get people I follow 
    following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
    i_follow = User.objects.filter(id__in=following_ids)
    
    # Get mutual follows
    mutual_ids = Follow.objects.filter(follower=user, is_mutual=True).values_list('following_id', flat=True)

    # Follow-back suggestions 
    follow_back = my_followers.exclude(
        id__in=i_follow
    ).exclude(
        id__in=mutual_ids
    ).exclude(
        id=user.id
    )
    
    # Get IDs for exclusion
    follow_back_ids = follow_back.values_list('id', flat=True)
    
    friends_of_friends = User.objects.filter(
        followers__following__in=i_follow
    ).exclude(
        id=user.id
    ).exclude(
        id__in=follow_back_ids  # Fixed: using variable instead of inline values_list
    ).exclude(
        id__in=mutual_ids
    ).exclude(
        id__in=following_ids
    ).annotate(
        follower_count=Count('followers')
    ).order_by('follower_count')
    
    # Get more IDs for exclusion
    friends_of_friends_ids = friends_of_friends.values_list('id', flat=True)
    
    popular_users = User.objects.annotate(
        follower_count=Count('followers')
    ).exclude(
        id=user.id
    ).exclude(
        id__in=following_ids
    ).exclude(
        id__in=follow_back_ids
    ).exclude(
        id__in=friends_of_friends_ids
    ).order_by('-follower_count')[:3]

    # Convert querysets to lists and return
    return list(follow_back) + list(friends_of_friends) + list(popular_users)


def user_feed(request):

    six_months = timezone.now() - timedelta(days=180)
    three_months = timezone.now() - timedelta(days=90)

    seen_posts = Seen_Post.objects.filter(user=request.user)\
                    .values_list('post_id', flat=True)

    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)

    mutual_ids = Follow.objects.filter(
        follower=request.user,
        is_mutual=True
    ).values_list('following_id', flat=True)

    regular_ids = [uid for uid in following_ids if uid not in mutual_ids]

    unseen_posts = Post.objects.exclude(id__in=seen_posts)

    mutual_posts = unseen_posts.filter(
        user_id__in=mutual_ids,
        posted_at__gte=six_months.date()
    ).order_by('-likes_count','-comment_count' ,'-posted_at')[:3]

    regular_posts = unseen_posts.filter(
        user_id__in=regular_ids,
        posted_at__gte=six_months.date()
    ).order_by('-likes_count','-comment_count', '-posted_at')[:2]


    feed = list(mutual_posts) + list(regular_posts)

    return feed



def mark_as_seen(user,post):
    Seen_Post.objects.get_or_create(user=user,post=post)




