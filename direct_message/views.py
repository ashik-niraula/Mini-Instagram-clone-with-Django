from django.shortcuts import render,get_object_or_404,redirect
from post.models import Follow
from .models import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.

#message Inbox View
def inbox(request):
    friends = request.user.followers.filter(is_mutual=True)
    conversations = Conversation.objects.filter(
        user_1=request.user)| Conversation.objects.filter(
            user_2 = request.user).order_by('last_sent')
    
    data = request.GET.get('search')
    if data:
        conversations = conversations.filter(Q(user_1_username__icontains=data)|Q(user_2__username__icontains=data))
    context = {
        'conversations':conversations
    }
    
    return render(request,'inbox.html',context)

#Chat view
def dm(request,username):
    friends = request.user.followers.filter(is_mutual=True)
    other_user = get_object_or_404(User,username=username)
    
    #Filtering the previous Conversations If Exists
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
    
    Messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

   #for sending message
    if request.method == 'POST':
        if friends.filter(follower=other_user).exists():    
            text = request.POST.get('text')
            image = request.FILES.get('image')
    

            if text or image:

                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    text=text if text else '',  # Empty string if no text
                    image=image if image else None,
                )
            
                return redirect('dm', other_user.username)
        else:
            messages.error(request,"You both are no Longer friends")
    
    context = {
        'other_user': other_user,
        'Messages': Messages,
    }
    return render(request,'chat.html',context)


def delete_msg(request,id,username):
    message = get_object_or_404(Message,id=id)
    other_user = get_object_or_404(User,username=username)
    if message.sender == request.user:
        message.delete()
        return redirect('dm',other_user.username)

def edit_msg(request,id,username)    :
    message = get_object_or_404(Message,id=id)    
    other_user = get_object_or_404(User,username=username)
    if request.user == message.sender:
        if request.method == "POST":
            text = request.POST.get('text')
            if text:
                message.text = text
                message.save()
                return redirect('dm',username)
        context = {
            'message': message,
            "other_user": other_user
        }
        return render(request,'edit_chat.html',context)