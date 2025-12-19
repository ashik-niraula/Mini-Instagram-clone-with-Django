from django.urls import path
from profilee import views

urlpatterns = [
    path('<username>/',views.profile,name='profile'),
    path('edit-profile',views.edit_profile,name='edit'),
    path('following/<username>',views.following_page,name='following'),
    path('follower/<username>',views.follower_page,name='follower'),
    path('saved-post/<username>',views.saved_post,name='saved'), 
]
