from django.urls import path

from forum.views import HomePage, Login, tempview

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
    path('login', Login.as_view(), name='loginpage'),
    path('temp', tempview),
]