"""minor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site
from users import views as user_views
from event import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('login/', user_views.CustomLogin.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('facelogin/', user_views.TwoFactorAuth, name='twofactorauth'),
    path('facelogin/authenticate/', user_views.postFaceLogin, name='postfacelogin'),
    path('profile/', user_views.profile, name="profile"),
    path('profile/<int:pk>',
         user_views.ProfileDetailView.as_view(template_name='users/profile_page.html'), name="profile-page"),
    path('profile/webcam', user_views.webcam, name='webcam'),
    path('profile/headshot', user_views.postHeadShot, name='postheadshot'),
    path('', include('blog.urls')),
    path('Query/', include('quesans.urls')),
    path('follow/<int:pk>', user_views.follow, name='follow'),
    # path('follow_request/<int:pk>',
    #      user_views.follow_request, name='follow-request'),
    path('accept_request/<int:pk>',
         user_views.accept_follow_request, name='accept-follow-request'),
    path('find_friends/',
         user_views.findFriend, name='find-friend'),
    path('suggestions/', user_views.ProfileListView.as_view(
        template_name='users/suggestions.html'), name='suggestions'),
    path('tinymce/', include('tinymce.urls')),
    path('create_event/', event_views.EventCreateView.as_view(
        template_name='event/create.html'), name='create-event')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
