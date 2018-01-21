from django.contrib.auth.decorators import login_required
from django.urls import path

from forum.views import HomePage, Login, Logout, Register, AboutPage, DeletePost, RestorePost, DeletedPosts, EditPost, \
    DeleteReply, EditReply, MarkDownToHtml, EditUserProfile, UserList, RecentPostList
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
    path('users', UserList.as_view(), name='user_list'),
    path('recent-posts', RecentPostList.as_view(), name='recent_post_list'),

    # post only
    path('delete-post', login_required(DeletePost.as_view()), name='delete_post'),
    path('restore-post', login_required(RestorePost.as_view()), name='restore_post'),
    path('reply', login_required(CreateReply.as_view()), name='create_reply'),
    path('delete-reply', login_required(DeleteReply.as_view()), name='delete_reply'),
    path('markdown-to-html', login_required(MarkDownToHtml.as_view()), name='markdown_to_html'),
    path('logout', login_required(Logout.as_view()), name='logout'),

    # get and post
    path('login', Login.as_view(), name='loginpage'),
    path('register', Register.as_view(), name='registration_page'),
    path('edit-post', login_required(EditPost.as_view()), name='edit_post'),
    path('edit-reply', login_required(EditReply.as_view()), name='edit_reply'),
    path('edit-user', login_required(EditUserProfile.as_view()), name='edit_user'),
    path('create-post', login_required(CreatePost.as_view()),name='create_post'),
]