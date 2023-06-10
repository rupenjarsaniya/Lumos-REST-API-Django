from django.urls import path
from backend.views import userViews

userUrlpatterns = [
   path('create', userViews.create_user, name='create_user'),
   path('login', userViews.login, name='login'),
   path('delete', userViews.delete_user, name='delete_user'),
   path('update', userViews.update_user, name='update_user'),
   path('', userViews.get_user, name='get_user'),
] 