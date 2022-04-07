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
    pass    # active = request.GET.get('approved', False)
    # token_id = request.GET.get('id', False)
    # # first you get your Job model
    # token = Token_Book.objects.get(pk=token_id)
    # try:
    #     token.approved = 1
    #     token.save()
    #     return JsonResponse({"success": True})
    # except Exception as e:
    #     return JsonResponse({"success": False})
    # return JsonResponse(data)

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from rest_framework import status
from .models import *


def passwordResetView(request,uidb64, token):
    try:
        MIN_LENGTH = 8
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            
            messages.add_message(request, messages.constants.ERROR, 'Your link has been expired')
            return redirect('login1',token_valid="false")
        
        if request.method == "POST":
            # form = ResetPasswordForm(request.POST)
            password = request.POST["password1"]
            # At least MIN_LENGTH long
            if len(password) < MIN_LENGTH:
                return render(request, "recover-password.html", {'min_len': f"The new password must be at least {MIN_LENGTH} characters long."})

            # At least one letter and one non-letter
            first_isalpha = password[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in password):
                return render(request, "recover-password.html", {'min_len': "The new password must contain at least one letter and at least one digit or" \
                                            " punctuation character."})
            
            confirm_password = request.POST["password2"]

            if password != confirm_password:
                return render(request, "recover-password.html", {'Wrong': "Password Does not match"})
            # if(form.is_valid()):
                
            messages.add_message(request, messages.constants.SUCCESS, 'Your password changed Successfully')
            user.set_password(confirm_password)
            user.save()
            return redirect('login1',token_valid="true")
        return render(request, "recover-password.html", {'uidb64': uidb64})

    except DjangoUnicodeDecodeError as identifier:
        try:
            if not PasswordResetTokenGenerator().check_token(user):
                    return redirect('login1',token_valid="false")
            
        except UnboundLocalError as e:
            return HttpResponse({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
    
def ResetView(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('template', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            print(user.email)
            send_mail(
                'Reset Password',
                'To initiate the password reset process for your ' + user.username +
                ''' Django Registration/Login App Account,

                click the link below: ''' + absurl +

                ''' If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.

                Sincerely,
                The Developer''',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )                                                                  
            return render(request, 'registration/password_reset_form.html', {"EmailSend": "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder."})
        except User.DoesNotExist:
            messages.add_message(request, messages.constants.ERROR, 'Email Does not Exist')
            return redirect('reset')

    return render(request, 'registration/password_reset_form.html')


def login1(request,token_valid):
    if(token_valid=="false"):
        return render(request, 'home.html')

    return redirect('admin:login')


def error_404_view(request, exception):
    return render(request,'404.html')

def index(request):
    return render(request,'index.html')

def campus_student_detail(request,pk):
    que = Candidate.objects.filter(campus=pk)
    return render(request,'dummy.html',{'que':que})

def myview(request, id):
   display=Candidate.objects.get(pk=id)
   template_name='admin/base.html'
   context={'display':display}
   return render(request, template_name, context)

def resultEmail(request, email, candidate_name):
    send_mail(
    'Space-O Technologies On-Campus Recruitment Drive',
    'Hello '+ candidate_name + ''',
    
Great news! You have completed your assessment and Space-O Technologies has successfully received your results. 

What’s next?  The recruiter will now review your application and assessment results to determine if you will be moving to the next phase. If you will be moving forward in the process, we will contact you regarding next steps. 

We are very excited about your interest in our program and look forward to getting to know you better.

The Space-O Technologies HR team
    ''',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    ) 
    return True

