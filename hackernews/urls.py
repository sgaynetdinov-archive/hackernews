from django.urls import path

from .views import ListsPost

urlpatterns = [
    path('posts', ListsPost.as_view()),
]
