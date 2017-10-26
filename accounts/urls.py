from django.conf.urls import url, include
from django.contrib import admin
from .views import AccountsViews, LoginViews, LogoutViews, UserprofileViews
from django.contrib.auth.decorators import login_required


urlpatterns = [

    url(r'^register/', AccountsViews.as_view()),
    url(r'^login/', LoginViews.as_view()),
    url(r'^logout/', LogoutViews.as_view()),

    url(r'^userprofile/', UserprofileViews.as_view()),

]
