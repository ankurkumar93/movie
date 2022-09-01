from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('movie', views.MovieView.as_view(), name='movie'),
    path('collection', views.Collection.as_view(), name='collection'),
    path('collection/<collection_uuid>/', views.EditCollection.as_view(), name='editcollection'),
    path('request-count/', views.RequestCounter.as_view(), name='request-count'),
    path('request-count/reset/', views.ResetCounter.as_view(), name='request-count'),
]