from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from forum.models import Board, Post, Reply, UserProfile

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
    def get(self, request, board_id):
        """View list of (not deleted) posts of a page"""

        board = get_object_or_404(Board, pk=board_id)
        posts = board.post_set.filter(deleted=False).order_by('-creation_date')

        context= {
            'board' : board,
            'post_list' : posts
        }

        return render(request, 'forum/board_posts.html', context)

class PostDetail(View):
    """
        show the post's content and replies
    """
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        if not post.userIsAuthorizedToViewPost(request.user):
            return self.unauthenticatedUserResponse(request)

        context = {
            'post': post
        }

        return render(request, 'forum/post_detail.html', context)

    def unauthenticatedUserResponse(self, request):
        context={
            'msg_text' : 'Error: This post has been deleted.',
        }
        return render(request, 'forum/show_message.html', context)


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

        context = {
            'post_list' : Post.objects.filter(deleted=True).order_by('-creation_date')
        }

        return render(request, 'forum/deleted_posts.html', context)

# post only

class CreateReply(View):
    def post(self, request):
        reply_to_post_id= request.POST['reply_to_post_pk']
        reply_to= get_object_or_404(Post, pk=reply_to_post_id)
        user = request.user
        content = request.POST['content']

        Reply.objects.create(reply_to= reply_to, creator= user.userprofile, content= content)
        return redirect(reverse('forum:post_detail', args= [reply_to_post_id]) )

class DeletePost(View):
    def post(self, request):
        # todo add authorizaton code

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

    # todo complete validation, using model validators
    def post(self, request):
        POST = request.POST
        uname = POST['username']
        email= POST['email']
        pw= POST['passowrd']
        confirm_pw= POST['confirm_password']

        if pw != confirm_pw or User.objects.filter(username=uname).exists():
            context = {'show_registration_failed_msg': True}
            render(request, 'forum/registration_page.html', context)

        user = User(username= uname)
        user.set_password(pw)
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

        post = Post.objects.create(title=title, content=content, board=board, creator=user.userprofile)

        return redirect(reverse('forum:post_detail', args=[post.pk]))

class EditPost(View):
    def get(self, request):
        post_id = request.GET['post_id']
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if not post.userIsAuthorizedToEditPost(user):
            # todo redirect to a template with this message
            return HttpResponse('You are not authorized to edit this post.')

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
            # todo redirect to a template with this message
            return HttpResponse('You are not authorized to edit this post.')

        # todo do data validation
        post.title = POST['post_title']
        post.content = POST['post_content']
        post_to_board_id = int(POST['post_to_board_id'])

        board= get_object_or_404(Board, pk= post_to_board_id)
        post.board = board
        post.save()

        return redirect(reverse('forum:post_detail', args=[post.pk]))
