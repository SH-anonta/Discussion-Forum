from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from forum.models import Board, Post, Reply, UserProfile


class HomePage(View):
    def get(self, request):
        context = {
            'boards' : Board.objects.all()
        }
        return render(request, 'forum/home_page.html', context)

class AboutPage(View):
    def get(self, request):
        return render(request, 'forum/about_page.html')

class Login(LoginView):
    template_name= 'forum/login_page.html'
    extra_context = {}

    context_var_print_login_fail_msg= 'print_login_fail_msg'

    def get(self, request, *args, **kwargs):
        # If the user is already logged in, send them to homepage 
        if request.user.is_authenticated:
            return redirect('forum:homepage')

        self.extra_context[self.context_var_print_login_fail_msg]= False

        return super().get(request, args, kwargs)


    
    def post(self, request, *args, **kwargs):
        uname = request.POST['username']
        pw    = request.POST['password']
        user = authenticate(request, username= uname, password= pw)

        # If login fails, print login failed message in template
        self.extra_context[self.context_var_print_login_fail_msg]= user is None

        return super().post(request, args, kwargs)

class Logout(LogoutView):
    pass

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
        #todo check if post is deleted, if so check if user is authorized
        context = {
            'post': get_object_or_404(Post, pk=post_id)
        }

        return render(request, 'forum/post_detail.html', context)

class UserDetail(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        context={
            'user_profile' : user,
        }

        return render(request, 'forum/user_detail.html', context)

class CreateReply(View):
    def post(self, request):
        reply_to_post_id= request.POST['reply_to_post_pk']
        reply_to= get_object_or_404(Post, pk=reply_to_post_id)
        user = request.user
        content = request.POST['content']

        Reply.objects.create(reply_to= reply_to, creator= user.userprofile, content= content)
        return redirect(reverse('forum:post_detail', args= [reply_to_post_id]) )

class CreatePost(View):
    def get(self, request):
        """get the form page for creating a new post"""

        default_board = int(request.GET.get('board_id', '-1'))
        
        context= {
            'default_post_to' : default_board, 
            'boards' : Board.objects.all()
        }

        return render(request, 'forum/create_post_editor.html', context)
    
    def post(self, request):
        user = request.user

        board= get_object_or_404(Board, pk=request.POST['post_to_board_id'])
        
        # todo add validation using forms
        title = request.POST['post_title'].strip()
        content = request.POST['post_content'].strip()
        
        post = Post.objects.create(title= title, content=content, board=board, creator=user.userprofile)
        
        return redirect(reverse('forum:post_detail', args=[post.pk]))

class DeletePost(View):
    def post(self, request):
        # todo add authorizaton code
        # todo show post deleted message after operation

        post_id  = int(request.POST.get('post_id', '-1'))
        post = get_object_or_404(Post, pk= post_id)

        post.deleted= True
        post.save()

        return redirect(reverse('forum:board_posts', args=[post.board.pk]))

class RestorePost(View):
    def post(self, request):
        # todo add authorizaton code

        post_id  = int(request.POST.get('post_id', '-1'))
        post = get_object_or_404(Post, pk= post_id)

        post.deleted= False
        post.save()

        return redirect(reverse('forum:board_posts', args=[post.board.pk]))

class DeletedPosts(View):
    def get(self, request):
        # do authorization

        context = {
            'post_list' : Post.objects.filter(deleted=True)
        }

        return render(request, 'forum/deleted_posts.html', context)