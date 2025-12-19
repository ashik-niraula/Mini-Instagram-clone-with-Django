from post.views import *



# Create your views here.
def profile(request,username):
    user = get_object_or_404(User,username=username)
    profile = get_object_or_404(Profile,user=user)
    user_post = Post.objects.filter(user=user).order_by('-posted_at')

    following_ids = request.user.following.values_list('following_id',flat=True)
    follower_ids = request.user.followers.values_list('follower_id',flat=True)

    context = {
        'user_post':user_post,
        'profile':profile,
        'following_ids': following_ids,
        'follower_ids':follower_ids
    }


    return render(request,'profile.html',context)


@login_required(login_url='login')
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user == request.user:
        if request.method == 'POST':
            data = request.POST
            
            profile_image = request.FILES.get('image')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            bio = data.get('bio')
            location = data.get('location')
            website = data.get('website')
                
            request.user.first_name = first_name
            request.user.last_name = last_name
            profile.bio = bio
            profile.location = location
            profile.website = website
            if profile_image:
                profile.profile_image = profile_image
            profile.save()
            request.user.save()
            return redirect('profile' , profile.user.username)

        context = {
                'profile':profile
            }
        return render(request,'edit_profile.html',context)


@login_required(login_url='login')
def following_page(request,username):
    #whose profile
    user_obj = get_object_or_404(User,username=username)
    following_users = Follow.objects.filter(follower=user_obj).select_related('following')
    
    visiting_user_mutuals = Follow.objects.filter(follower=request.user,is_mutual=True).values_list('following_id',flat=True)
    visiting_user_following = Follow.objects.filter(follower=request.user).values_list('following_id',flat=True)
    visiting_user_follower = Follow.objects.filter(following=request.user).values_list('follower_id',flat=True)
    
    data = request.GET.get('search')
    if data:
        following_users = following_users.filter(following__username__icontains=data)


    context = {
        'following_users':following_users,
        'user_obj': user_obj,
        'visiting_user_mutuals': visiting_user_mutuals,
        'visiting_user_following': visiting_user_following,
        'visiting_user_follower': visiting_user_follower,
    }
        

    return render(request,'following.html',context)    

@login_required(login_url='login')  
def follower_page(request,username):
    user_obj  = get_object_or_404(User,username=username)
    followers = Follow.objects.filter(following=user_obj).select_related('follower')
    
    
    req_mutuals = request.user.followers.filter(following=request.user,is_mutual=True).values_list('follower_id',flat=True)
    req_following = request.user.following.values_list('following_id',flat=True)
    req_followers = request.user.followers.values_list('follower_id',flat=True)
    

    data = request.GET.get('search')
    if data:
        followers = followers.filter(follower__username__icontains=data)


    context = {
        'req_mutuals':req_mutuals,
        'req_following':req_following,
        'req_followers':req_followers,
        'user_obj': user_obj,
        'followers': followers
    }
    return render(request,'follower.html',context)    

@login_required(login_url='login')
def saved_post(request,username):
    profile = get_object_or_404(Profile,user__username=username)
    saved_posts = Saved_Post.objects.filter(user__username=username)
    context = {
        'profile':profile,
        'saved_posts':saved_posts
    }
    return render(request,'saved_post.html',context)