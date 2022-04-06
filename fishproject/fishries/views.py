from django.shortcuts import render
from django.contrib import auth

# Create your views here.
def home(request):
    # if request.method == "POST":
    #     user = auth.authenticate(username = request.POST('username'))
    #     password = request.POST('password')

    #     if user is not None:
    #         auth.login(request, user)
    #         return render(request,'registration.html')
    #     else:
    #         return render(request,'login.html',{'error':'Username or password is Invalid'})
    
    return render(request, 'widgets.html')
