from django.urls import path

from forum.views import HomePage, Login, Logout, Register, AboutPage, BoardPosts, PostDetail, UserDetail, CreateReply

app_name= 'forum'
urlpatterns = [
    path('', HomePage.as_view(), name= 'homepage'),
    path('about', AboutPage.as_view(), name='about_page'),
    path('board/<int:board_id>', BoardPosts.as_view(), name='board_posts'),
    path('post/<int:post_id>', PostDetail.as_view(), name='post_detail'),
    path('user/<int:user_id>', UserDetail.as_view(), name='user_detail'),

    path('reply', CreateReply.as_view(), name='create_reply'),
    path('login', Login.as_view(), name='loginpage'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='registration_page'),
]