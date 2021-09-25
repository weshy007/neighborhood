from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='index' ),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('hoods/',views.hoods,name = 'hoods'),
    path('single_hood/<hood_id>',views.single_hood,name = 'single_hood'),
    path('results/',views.search_profile,name = 'results'),
    path('join_hood/<id>',views.join,name='join'),
    path('leave_hood/<id>',views.leave,name='leave'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/users/', views.UserList.as_view()),
]