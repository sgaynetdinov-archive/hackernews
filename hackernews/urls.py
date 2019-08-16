from django.urls import re_path, include
from rest_framework import routers

from .views import ListsPost

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'posts', ListsPost, basename='Posts')

urlpatterns = [
    re_path('^', include(router.urls)),
]
