from django.urls import path,include
from post import views

urlpatterns = [
    path('',views.homepage,name='home'),
    
    path('detail/<uuid:post_id>/', views.detail_view, name='detail'),

    path('upload/', views.upload_post, name='upload'),
    path('edit-post/<post_id>', views.edit_post, name='edit-post'),
    path('delete-post/<post_id>', views.delete_post, name='delete-post'),

    path('follow/<user_id>/', views.follow_unfollow, name='follow'),
    path('suggestions/', views.suggestion_page, name='suggestion'),
    
    path('signup/',views.signup_page,name='signup'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'), 

    path('friends/',views.friends_page,name='friends'), 

    path('likes/<uuid:post_id>',views.likes_page,name='likes'), 
    path('like/<uuid:post_id>/', views.like_post, name='like'),

    path('save-post/<uuid:post_id>/',views.save_delete_post,name='save'), 

    path('delete-comment/<comment_id>/',views.delete_comment,name='del-comment'), 
    path('edit-comment/<comment_id>/',views.edit_comment,name='edit-comment'), 

    path('see-more/',views.see_more,name='seemore'), 
    path('reset-see-more/',views.reset_see_more,name='reset-seemore'), 
    
     
]
