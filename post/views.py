from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .utils import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from profilee.models import Profile


# Create your views here.

@login_required(login_url='signup')
def homepage(request):
    # Generate user feed
    feed_posts = user_feed(request)
    suggestions = follow_suggestions(request.user)

    following_ids = request.user.following.values_list('following_id',flat=True)
    follower_ids = request.user.followers.values_list('follower_id',flat=True)
    friends = request.user.following.filter(is_mutual=True)
    
    current_post_ids = [str(post.id) for post in feed_posts]
    request.session['current_post_ids'] = current_post_ids
    seen_posts = Seen_Post.objects.filter(user=request.user).exists()

    liked_post_ids = request.user.likes.values_list('post_id', flat=True)
    saved_post_ids = request.user.user_saving.values_list('post_id',flat=True)

    
    context =  {'feed_posts': feed_posts,
                'liked_post_ids':liked_post_ids,
                'saved_post_ids': saved_post_ids,
                'suggestions':suggestions[:5],
                'follower_ids': follower_ids,
                'following_ids': following_ids,
                'friends': friends[:3],
                'seen_posts': seen_posts,
                }

    return render(request, 'home.html',context)


@login_required(login_url='login')
def see_more(request):
    # Get current post IDs from session
    current_post_ids = request.session.get('current_post_ids', [])
    if current_post_ids:
        for post_id in current_post_ids:
            post = get_object_or_404(Post,id=post_id)
            mark_as_seen(request.user,post)
        
    return redirect('home')

@login_required(login_url='login')
def reset_see_more(request):
    seen_post = Seen_Post.objects.filter(user=request.user)
    seen_post.delete()
    return redirect('home')
    
@login_required(login_url='login')    
def friends_page(request):
    friends = request.user.followers.filter(is_mutual=True)
    req_mutuals = request.user.followers.filter(following=request.user,is_mutual=True).values_list('follower_id',flat=True)
    req_following = request.user.following.values_list('following_id',flat=True)
    req_followers = request.user.followers.values_list('follower_id',flat=True)
    data = request.GET.get('search')
    if data:
        friends = friends.filter(follower__username__icontains=data)
    context = {
        'req_mutuals':req_mutuals,
        'req_following':req_following,
        'req_followers':req_followers,
        'friends':friends
    }
    

    return render(request,'friends.html',context)

@login_required(login_url='login')
def upload_post(request):
    if request.method == "POST":
        data = request.POST
        user = request.user
        caption = data.get('caption')
        image = request.FILES.get('image')

        post = Post.objects.create(
            user = user,
            caption = caption,
            image = image
        )

        post.extract_hagtags()
        return redirect('home')
    return render(request,'upload_post.html')

@login_required(login_url='login')
def edit_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if post.user == request.user:
        if request.method == "POST":
            data = request.POST
            caption = data.get('caption')
            image = request.FILES.get('image')

            post.caption = caption
            if image:
                post.image = image
            post.save()    
            return redirect('detail',post.id)
        context ={
            "post": post
        }
        return render(request,'edit_post.html',context)
    else:
        return render(request,'home.html')

@login_required(login_url='login')
def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('profile', post.user.username)
    else:
        logout(request)
    

def suggestion_page(request):
    suggestions = follow_suggestions(request.user)

    following_ids = request.user.following.values_list('following_id',flat=True)
    follower_ids = request.user.followers.values_list('follower_id',flat=True)
    
    context ={
        'suggestions': suggestions,
        'following_ids':following_ids,
        'follower_ids': follower_ids,
    }
    return render(request,'suggestion.html',context)    


@login_required(login_url='login')
def follow_unfollow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    current_user = request.user

    
    if Follow.objects.filter(follower=current_user, following=user_to_follow).exists():
        # Unfollow
        
        if Follow.objects.filter(follower=user_to_follow, following=current_user).exists():
            Follow.objects.filter(follower=current_user, following=user_to_follow).delete()
            before_status = 'Unfollow'
            after_status = 'Follow_back'
        else:
            Follow.objects.filter(follower=current_user, following=user_to_follow).delete()
            before_status = 'Following'
            after_status = 'Follow'

    elif Follow.objects.filter(follower=user_to_follow, following=current_user).exists():
        # Follow back scenario
        Follow.objects.create(follower=current_user, following=user_to_follow)
        before_status = 'Follow_back'
        after_status = 'Friends'
    else:
        # Regular follow
        Follow.objects.create(follower=current_user, following=user_to_follow)
        before_status = 'Follow'
        after_status = 'Following'

    return JsonResponse({
        'before_status': before_status,
        'after_status': after_status
    })

@login_required(login_url='login')
def like_post(request, post_id):
        # Get the post
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user already liked this post
        like_exists = Like.objects.filter(user=request.user, post=post).exists()
        
        if like_exists:
           
            Like.objects.filter(user=request.user, post=post).delete()
            liked = False
        else:
            
            Like.objects.create(user=request.user, post=post)
            liked = True    
        
        
        post.update_like_count()
        return JsonResponse({
            'liked':liked,
            "count":post.likes_count
        })

@login_required(login_url='login')
def likes_page(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    users_liked = Like.objects.filter(post=post)
    data = request.GET.get('search')
    if data:
        users_liked = users_liked.filter(user__username__icontains=data)
    context = {
        'users_liked':users_liked
    }
    return render(request,'likes.html',context)
        
@login_required(login_url='login')
def detail_view(request,post_id):
    post = get_object_or_404(Post,id=post_id)

    liked_post_ids = request.user.likes.values_list('post_id',flat=True)

    comments = Comment.objects.filter(post=post).order_by('-created_at')

    saved_post_ids = Saved_Post.objects.filter(user=request.user).values_list('post_id',flat=True)
    if request.method == "POST":
        comment = request.POST.get('comment')

        Comment.objects.create(
            user =request.user,
            post = post,
            text = comment
        )
        return redirect('detail',post_id)
    
    
    context = {
        'post':post,
        'liked_post_ids':liked_post_ids,
        'comments': comments,
        'saved_post_ids':saved_post_ids
    }

    return render(request,'details.html',context)

@login_required(login_url='login')
def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    post_id = comment.post.id
    if comment.user == request.user or comment.post.user == request.user:
        comment.delete()
        return redirect('detail',post_id)
    else:
        logout(request) 
    
@login_required(login_url='login')    
def edit_comment(request,comment_id):
    user_comment = get_object_or_404(Comment,id=comment_id)
    profile = get_object_or_404(Profile,user=user_comment.user)
    post = get_object_or_404(Post,id=user_comment.post.id)

    comments = Comment.objects.filter(post=post).order_by('-created_at')
    liked_post_ids = request.user.likes.values_list('post_id',flat=True)
    saved_post_ids = request.user.user_saving.values_list('post_id',flat=True)


    if user_comment.user == request.user:
        if request.method == "POST":
            text = request.POST.get('comment')
            user_comment.text = text
            user_comment.save()
            
            
            return redirect('detail',user_comment.post.id)
        
        
        context ={
            'user_comment':user_comment,
            'comments': comments,
            "profile": profile,
            "post":post,
            "liked_post_ids": liked_post_ids,
            "saved_post_ids": saved_post_ids

        }
        return render(request,'edit_comment.html',context)
    else:
        logout(request)

@login_required(login_url='login')
def comments_page(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    users_commented = Comment.objects.filter(post=post)
    data = request.GET.get('search')
    if data:
        users_commented = users_commented.filter(user__username__icontains=data)
    context = {
        'users_liked':users_commented
    }
    context = {
        'users_commented':users_commented
    }
    return render(request,'comment.html',context)        

@login_required(login_url='login')        
def save_delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    saved_post , created = Saved_Post.objects.get_or_create(user=request.user,post=post)
    if created:
        saved = True
    else:
        saved_post.delete()   
        saved = False
    return JsonResponse({
        'saved':saved
    })     


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password1') 
        password2 = data.get('password2')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        
        # Validate passwords match
        if password != password2:
            messages.error(request, "Your Passwords Didn't Match")
            return redirect('signup')
        
        # Check for existing username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        # Check for existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        # Create user if all checks pass
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            messages.success(request, 'You have successfully Registered')
            login(request, user)
            Profile.objects.create(
                user = user
            )
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('signup')
    
    return render(request, 'signup.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        password = data.get('password')
        if 'username' in data:
            username = data.get('username')
            user = authenticate(username=username,password=password)
        elif 'email' in data:
            email = data.get('email')
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username,password=password)
            except User.DoesNotExist:
                user = None
                  
        if user is not None:
            login(request,user)
            return redirect('home') 
        if user is None:
            messages.error(request,"Invalid Credintials")
            return redirect('login')       
        
         
    return render(request,'login.html') 

@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')