from django.urls import path

from forum.views import HomePage, Login, Logout, Register, AboutPage, BoardPosts

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
    path('about', AboutPage.as_view(), name='about_page'),
    path('board/<int:board_id>', BoardPosts.as_view(), name='board_posts'),

    path('login', Login.as_view(), name='loginpage'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='registration_page'),
]