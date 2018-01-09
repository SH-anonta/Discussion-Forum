from django.urls import path
from forum.views import HomePage

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
]