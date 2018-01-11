from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class HomePage(View):
    def get(self, request):
        return render(request, 'forum/home_page.html')

class Login(LoginView):
    template_name= 'forum/login_page.html'
    
    def get(self, request, *args, **kwargs):
        # If the user is already logged in, send them to homepage 
        if request.user.is_authenticated:
            return redirect('forum:homepage')
        
        return super().get(request, args, kwargs)
    
    
class Logout(LogoutView):
    pass
