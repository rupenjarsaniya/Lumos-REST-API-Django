from django.urls import path
from backend.views import taskViews

taskUrlpatterns = [
   path('create', taskViews.create_task, name='create_task'),
   path('', taskViews.get_task, name='get_task'),    
   path('delete/<str:id>', taskViews.delete_task, name='delete_task'),
   path('update/<str:id>', taskViews.update_task, name='update_task'),
   path('<str:id>', taskViews.get_task_by_id, name='get_task_by_id'),
] 