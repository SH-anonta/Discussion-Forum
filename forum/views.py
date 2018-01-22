from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from forum.models import Board, Post, Reply, UserProfile
from forum.utility import MarkdownToHtmlConverter

# get only
class HomePage(View):
    def get(self, request):
        context = {
            'boards' : Board.objects.all()
        }
        return render(request, 'forum/home_page.html', context)

class AboutPage(View):
    def get(self, request):
        return render(request, 'forum/about_page.html')

class BoardPosts(View):
    POSTS_PER_PAGE= 20

    def get(self, request, board_id):
        """View list of (not deleted) posts of a page"""

        board = get_object_or_404(Board, pk=board_id)
        posts = board.post_set.filter(deleted=False).order_by('-creation_date')

        paginator = Paginator(posts, self.POSTS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        post_list = paginator.get_page(page_number)

        context= {
            'board' : board,
            'post_list' : post_list
        }

        return render(request, 'forum/board_posts.html', context)

#todo send show_edit_options variable to templates and remove permission checking in templates
class PostDetail(View):
    """
        show the post's content and replies
    """
    REPLY_PER_PAGE= 10

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        if not post.userIsAuthorizedToViewPost(request.user):
            return self.unauthenticatedUserResponse(request)

        all_replies = post.reply_set.order_by('creation_date')
        paginator = Paginator(all_replies, self.REPLY_PER_PAGE)
        page_number= request.GET.get('page', 1)
        reply_list = paginator.get_page(page_number)

        context = {
            'post': post,
            'reply_list' : reply_list
        }

        return render(request, 'forum/post_detail.html', context)

    def unauthenticatedUserResponse(self, request):
        context={
            'msg_text' : 'Error: This post has been deleted.',
        }
        return render(request, 'forum/show_message.html', context)

#todo send show_edit_options variable to templates and remove permission checking in templates
class UserDetail(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        context={
            'user_profile' : user,
        }

        return render(request, 'forum/user_detail.html', context)

class DeletedPosts(View):
    def get(self, request):
        # do authorization

        if not self.userIsAuthorizedToViewPage(request.user):
            return self.unAuthorizedViewerResponse(request)

        context = {
            'post_list' : Post.objects.filter(deleted=True).order_by('-creation_date')
        }

        return render(request, 'forum/deleted_posts.html', context)

    def userIsAuthorizedToViewPage(self, user):
        return user.is_staff

    def unAuthorizedViewerResponse(self, request):
        context = {
            'msg_text' : 'You do not have permission to view this page.'
        }

        return render(request, 'forum/show_message.html', context)

class RecentPostList(View):
    POSTS_PER_PAGE = 20
    def get(self, request):
        posts = Post.objects.filter(deleted=False).order_by('-creation_date')

        paginator = Paginator(posts, self.POSTS_PER_PAGE )

        page_number = request.GET.get('page', 1)

        context= {
            'post_list' : paginator.get_page(page_number),
        }

        return render(request, 'forum/recent_post_list.html', context)

class UserList(View):
    USERS_PER_PAGE= 20

    def get(self, request):
        users = User.objects.order_by('username')
        paginator = Paginator(users, self.USERS_PER_PAGE)

        page_number = request.GET.get('page', 1)
        user_ist= paginator.get_page(page_number)

        context= {
            'user_list' : user_ist
        }

        return render(request, 'forum/user_list.html', context)

# post only

class CreateReply(View):
    def post(self, request):
        #todo add authorization, only admins should be able to create replies on deleted posts
        reply_to_post_id= request.POST['reply_to_post_pk']
        reply_to= get_object_or_404(Post, pk=reply_to_post_id)
        user = request.user
        content = request.POST['content']

        reply = Reply(reply_to= reply_to, creator= user.userprofile)
        reply.updateContent(content)
        reply.save()

        url = reverse('forum:post_detail', args= [reply_to_post_id])
        redirect_url = '%s?page=999999'
        # after reply is created, go to the last page of post_detail (where this reply can be seen)
        return redirect(redirect_url % (url,))

class DeletePost(View):
    def post(self, request):
        post_id = int(request.POST.get('post_id', '-1'))
        post = get_object_or_404(Post, pk=post_id)

        if not post.userIsAuthorizedToDeletePost(request.user):
            return HttpResponse('you are not allowed to delete this post')

        post.deleted = True
        post.save()

        return self.getSuccessResponse(request)

    def getSuccessResponse(self, request):
        context = {
            'msg_text': 'Post deleted successfully',
        }

        return render(request, 'forum/show_message.html', context)

class Logout(LogoutView):
    pass

class RestorePost(View):
    def post(self, request):
        if not request.user.is_staff:
            return self.showAuthorizationError(request)

        post_id  = int(request.POST.get('post_id', '-1'))
        post = get_object_or_404(Post, pk= post_id)

        post.deleted= False
        post.save()

        return redirect(reverse('forum:post_detail', args=[post.pk]))

    def showAuthorizationError(self, request):
        context= {
            'msg_text': 'You are not authorized to restore this post.'
        }

        return render(request, 'forum/show_message.html', context)

class DeleteReply(View):
    def post(self, request):
        reply_id= int(request.POST.get('reply_id', -1))
        reply= get_object_or_404(Reply, pk= reply_id)

        container_post_id = reply.reply_to.pk

        if not reply.userAuthorizedToDeleteReply(request.user):
            return self.unAuthorizedUserResponse(request)

        reply.delete()

        return redirect(reverse('forum:post_detail', args=[container_post_id]))

    def unAuthorizedUserResponse(self, request):
        context={
            'msg_text' : 'You do not have permission to delete this post.'
        }

        return render(request, 'forum/show_message.html', context)

# get and post

class Login(LoginView):
    template_name = 'forum/login_page.html'
    extra_context = {}

    context_var_print_login_fail_msg = 'print_login_fail_msg'

    def get(self, request, *args, **kwargs):
        # If the user is already logged in, send them to homepage
        if request.user.is_authenticated:
            return redirect('forum:homepage')

        self.extra_context[self.context_var_print_login_fail_msg] = False

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        uname = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username=uname, password=pw)

        # If login fails, print login failed message in template
        self.extra_context[self.context_var_print_login_fail_msg] = user is None

        return super().post(request, args, kwargs)

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('forum:homepage')

        context= {'show_registration_failed_msg': False}
        return render(request, 'forum/registration_page.html', context)

    # todo complete data validations
    def post(self, request):
        POST = request.POST
        uname = POST['username']
        email= POST['email']
        pw= POST['password']
        confirm_pw= POST['confirm_password']

        if pw != confirm_pw or User.objects.filter(username=uname).exists():
            context = {'show_registration_failed_msg': True}
            render(request, 'forum/registration_page.html', context)

        user = User(username= uname)
        user.set_password(pw)
        user.email= email
        user.save()

        UserProfile.objects.create(user= user)

        return redirect('forum:loginpage')

class CreatePost(View):
    def get(self, request):
        """get the form page for creating a new post"""

        default_board = int(request.GET.get('board_id', '-1'))

        context = {
            'default_post_to': default_board,
            'boards': Board.objects.all()
        }

        return render(request, 'forum/create_post_editor.html', context)

    def post(self, request):
        user = request.user

        board = get_object_or_404(Board, pk=request.POST['post_to_board_id'])

        # todo add validation using forms
        title = request.POST['post_title'].strip()
        content = request.POST['post_content'].strip()

        post = Post(title=title, board=board, creator=user.userprofile)
        post.updateContent(content)
        post.save()

        return redirect(reverse('forum:post_detail', args=[post.pk]))

# todo add authorizations: only admins can change the post's board
class EditPost(View):
    def get(self, request):
        post_id = request.GET['post_id']
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if not post.userIsAuthorizedToEditPost(user):
            return self.unAuthorizedUserResponse(request)

        boards= Board.objects.all()

        context = {
            'post' : post,
            'boards' : boards,
        }

        return render(request, 'forum/edit_post_editor.html', context)

    def post(self, request):
        POST= request.POST

        post_id = int(POST['post_id'])
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if not post.userIsAuthorizedToEditPost(user):
            return self.unAuthorizedUserResponse(request)

        # todo do data validation
        post.title = POST['post_title']
        content = POST['post_content']
        post.updateContent(content)
        post_to_board_id = int(POST['post_to_board_id'])

        board= get_object_or_404(Board, pk= post_to_board_id)
        post.board = board
        post.save()

        return redirect(reverse('forum:post_detail', args=[post.pk]))

    def unAuthorizedUserResponse(self, request):
        context={
            'msg_text' : 'You do not have permission to edit this post.'
        }

        return render(request, 'forum/show_message.html', context)

class EditReply(View):

    def get(self, request):
        reply_id = request.GET.get('reply_id', )
        reply = get_object_or_404(Reply, pk=reply_id)

        if not reply.userAuthorizedToEditReply(request.user):
            return self.unAuthorizedUserResponse(request)

        context= {
            'reply' : reply
        }

        return render(request, 'forum/edit_reply_editor.html', context)

    def post(self, request):
        # todo do data validation

        POST = request.POST
        reply_id = POST.get('reply_id', -1)
        reply = get_object_or_404(Reply, pk=reply_id)

        if not reply.userAuthorizedToEditReply(request.user):
            return self.unAuthorizedUserResponse(request)

        content = POST['reply_content']
        reply.updateContent(content)
        reply.save()

        containing_post_id = reply.reply_to.pk
        return redirect(reverse('forum:post_detail', args=[containing_post_id ]))

    def unAuthorizedUserResponse(self, request):
        context={
            'msg_text' : 'You do not have permission to edit this reply.'
        }

        return render(request, 'forum/show_message.html', context)

class MarkDownToHtml(View):
    def post(self, request):
        md = request.POST['md_text']
        html= MarkdownToHtmlConverter.convert(md)

        return HttpResponse(html)

class EditUserProfile(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk= user_id)

        if not user.userprofile.userAuthorizedToEditUser(request.user):
            return self.unauthorizedUserResponse(request)

        context={
            'user_profile' : user,
        }

        return render(request, 'forum/edit_user_editor.html', context)
    
    def post(self, request, user_id):
        POST = request.POST

        user = get_object_or_404(User, pk= user_id)

        if not user.userprofile.userAuthorizedToEditUser(request.user):
            return self.unauthorizedUserResponse(request)

        # todo do data validation
        
        user.email= POST['email']
        new_pw=  POST['new_password']
        confirm_pw=  POST['confirm_password']
        
        if new_pw != "":
            if new_pw != confirm_pw:
                return HttpResponse('passwords do not match')
            
            user.set_password(new_pw)

        user.save()
        
        return redirect(reverse('forum:user_detail', args=[user.id]))

    def unauthorizedUserResponse(self, request):
        context={
            'msg_text' : 'You do not have permission to edit user profiles.'
        }

        return render(request, 'forum/show_message.html', context)

