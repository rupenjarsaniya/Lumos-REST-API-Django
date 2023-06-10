from django.urls import path, include
from backend.urls.userUrls import userUrlpatterns
from backend.urls.taskUrls import taskUrlpatterns

urlpatterns = [
  path("user/", include(userUrlpatterns)),
  path("task/", include(taskUrlpatterns))
] 