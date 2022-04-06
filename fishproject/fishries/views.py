from django.shortcuts import render
from django.contrib import auth
from django.http import JsonResponse
from .models import *

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


def ajax_change_status(request):
    active = request.GET.get('approved', False)
    token_id = request.GET.get('id', False)
    # first you get your Job model
    token = Token_Book.objects.get(pk=token_id)
    try:
        token.approved = 1
        token.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})
    return JsonResponse(data)
