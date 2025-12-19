from django.urls import path
from direct_message import views

urlpatterns = [
    path('',views.inbox,name='inbox'),

    path('chat/<username>',views.dm,name='dm'),
]
