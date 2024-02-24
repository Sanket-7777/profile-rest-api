from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profile_api import views
from .views import fetch_tweets



router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet )
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
    path('tweets/', fetch_tweets, name='fetch_tweets'),
]
