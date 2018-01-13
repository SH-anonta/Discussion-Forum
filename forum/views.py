from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views import View

from forum.models import User, Board, Post


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
        post = request.POST
        uname = post['username']
        email= post['email']
        pw= post['passowrd']
        confirm_pw= post['confirm_password']

        if pw != confirm_pw or User.objects.filter(username=uname).exists():
            context = {'show_registration_failed_msg': True}
            render(request, 'forum/registration_page.html', context)

        user = User(username= uname)
        user.set_password(pw)
        user.save()

        return redirect('forum:loginpage')


class BoardPosts(View):
    def get(self, request, board_id):
        """View list of posts of a page"""
        board = Board.objects.get(pk=board_id)
        posts = board.post_set.all()

        context= {
            'board_posts' : posts
        }

        return render(request, 'forum/board_posts.html', context)

class PostDetail(View):
    """
        show the post's content and replies
    """
    def get(self, request, post_id):
        context = {
            'post': get_object_or_404(Post, pk=post_id)
        }

        return render(request, 'forum/post_detail.html', context)