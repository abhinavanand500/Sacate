from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('profile',views.profile,name='profile'),
    path('delete',views.deleteacc,name='deleteaccount'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('about',views.about,name='about'),
    path('tweet',views.tweet),
    path('acceptFood/<int:slug>', views.acceptFood),
    path('acceptCloth/<int:slug>', views.acceptCloth),
    path('dashboard',views.dashboard),
    path('profile/<str:slug>',views.viewprofile,name='about'),
    path('create-tweet',views.createtweet),
    path('search',views.search,name='search'),
    path('handleSignup',views.handleSignup,name='handleSignup'),
    path('handleLogin',views.handleLogin,name='handleLogin'),
    path('handleLogout',views.handleLogout,name='handleLogout'),
    path('donateFood',views.donateFood,name='donateFood'),
    path('donateCloth',views.donateCloth,name='donateCloth'),
    path('notify',views.notify,name='donateCloth'),
    path('donateOther',views.donateOther,name='donateOther'),
    path('acceptOther/<int:slug>',views.acceptOther,name='acceptOther'),
    path('acceptedOrder',views.acceptedOrder,name='acceptedOrder'),
]
