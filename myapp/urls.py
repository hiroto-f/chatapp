from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('username_change/<int:user_id>/', views.change_name, name='username_change'),
    path('username_change_done/', views.username_change_done,name='username_change_done'),
    path('mail_change/<int:user_id>/', views.mail_change, name='mail_change'),
    path('mail_change_done/', views.mail_change_done, name='mail_change_done'),
    path('icon_change/<int:user_id>/',views.icon_change, name='icon_change'),
    path('icon_change_done/', views.icon_change_done, name='icon_change_done'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/',views.Password_change.as_view(), name='password_change'),
    path('find/',views.find, name='find'),
]
