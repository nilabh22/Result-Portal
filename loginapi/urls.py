from knox import views as knox_views
from .views import loginPage,RegisterAPI
from django.urls import path
from loginapi import views

urlpatterns = [
    path('api/login/', views.loginPage, name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/file_upload/', views.FileUploadView.as_view(),name="upload")
]