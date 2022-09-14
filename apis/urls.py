from django.urls import path
from .views import Query

urlpatterns = [
    path('', Query.as_view(), name='query'),
]
