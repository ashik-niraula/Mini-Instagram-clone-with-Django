from django.shortcuts import render,get_object_or_404,redirect
from post.models import Follow
from .models import *
from django.db.models import Q

# Create your views here.
def inbox(request):
    friends = request.user.followers.filter(is_mutual=True)
    conversations = Conversation.objects.filter(
        user_1=request.user)| Conversation.objects.filter(
            user_2 = request.user).order_by('last_sent')
    
    context = {
        'conversations':conversations
    }
    
    return render(request,'inbox.html',context)

def dm(request,username):
    friends = request.user.followers.filter(is_mutual=True)
    other_user = get_object_or_404(User,username=username)
    
    conversation = Conversation.objects.filter(user_1=request.user,user_2=other_user).first()
    if not conversation:
        conversation = Conversation.objects.filter(user_1=other_user,user_2=request.user).first()
    if not conversation:
        if request.user != other_user:
            conversation = Conversation.objects.create(
                user_1=request.user,
                user_2 = other_user
        )
        else:
            return redirect('profile', request.user.username)
    
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        
        if text or image:  # Allow either text or image
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text if text else '',  # Empty string if no text
                image=image if image else None,
            )
        
        return redirect('dm', other_user.username)
    data = request.GET.get('search')
    if data:
        pass

    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request,'chat.html',context)


