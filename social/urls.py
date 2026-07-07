from django.urls import path
from . import views

urlpatterns = [

    path('', views.splash),

    path('login/', views.login),

    path('register/', views.register),

    path('home/', views.home),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

    path('logout/', views.logout),

    path('profile/<int:user_id>/', views.profile),

    path('follow/<int:user_id>/', views.follow_user),
    
    path('edit-profile/', views.edit_profile),

   path('search/', views.search, name='search'),

   path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

   path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
   
   path('notifications/', views.notifications, name='notifications'),

   path('followers/<int:user_id>/', views.followers, name='followers'),
   
   path('following/<int:user_id>/', views.following, name='following'),
]