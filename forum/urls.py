from django.urls import path

from forum.views import HomePage, Login, Logout, Register, AboutPage

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
    path('login', Login.as_view(), name='loginpage'),
    path('about', AboutPage.as_view(), name='about_page'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='registration_page'),
]