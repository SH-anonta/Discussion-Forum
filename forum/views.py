from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class HomePage(View):
    def get(self, request):
        return render(request, 'forum/home_page.html')

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
