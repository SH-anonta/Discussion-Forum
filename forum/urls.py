from django.contrib.auth.decorators import login_required
from django.urls import path

from forum.views import HomePage, Login, Logout, Register, AboutPage, DeletePost, RestorePost, DeletedPosts, EditPost, \
    DeleteReply, EditReply
from forum.views import CreatePost, BoardPosts, PostDetail, UserDetail, CreateReply

app_name= 'forum'
urlpatterns = [
    # get only
    path('', HomePage.as_view(), name= 'homepage'),
    path('about', AboutPage.as_view(), name='about_page'),
    path('board/<int:board_id>', BoardPosts.as_view(), name='board_posts'),
    path('post/<int:post_id>', PostDetail.as_view(), name='post_detail'),
    path('user/<int:user_id>', UserDetail.as_view(), name='user_detail'),
    path('deleted-posts', login_required(DeletedPosts.as_view()), name='deleted_posts'),

    # post only
    path('delete-post', login_required(DeletePost.as_view()), name='delete_post'),
    path('restore-post', login_required(RestorePost.as_view()), name='restore_post'),
    path('create-post', login_required(CreatePost.as_view()),name='create_post'),
    path('reply', login_required(CreateReply.as_view()), name='create_reply'),
    path('delete-reply', login_required(DeleteReply.as_view()), name='delete_reply'),

    path('logout', login_required(Logout.as_view()), name='logout'),

    # get and post
    path('login', Login.as_view(), name='loginpage'),
    path('register', Register.as_view(), name='registration_page'),
    path('edit-post', login_required(EditPost.as_view()), name='edit_post'),
    path('edit-reply', login_required(EditReply.as_view()), name='edit_reply'),
]