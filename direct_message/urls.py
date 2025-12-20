from django.urls import path
from direct_message import views

urlpatterns = [
    path('',views.inbox,name='inbox'),

    path('chat/<username>',views.dm,name='dm'),

    path('delete/<id>/<username>',views.delete_msg,name='delete-message'),
    path('edit/<id>/<username>',views.edit_msg,name='edit-message'),
]
