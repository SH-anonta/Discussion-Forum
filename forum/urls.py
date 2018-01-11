from django.urls import path

from forum.views import HomePage, Login, tempview, Logout

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
    path('login', Login.as_view(), name='loginpage'),
    path('logout', Logout.as_view(), name='logout'),
    path('temp', tempview),
]