from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomePage(View):
    def get(self, request):
        return render(request, 'forum/home_page.html')

class Login(LoginView):
    template_name= 'forum/login_page.html'

def tempview(request):
    # todo remove view
    if request.user.is_authenticated:
        return HttpResponse('Logged in as ' + request.user.username)
    else:
        return HttpResponse('Not logged in')