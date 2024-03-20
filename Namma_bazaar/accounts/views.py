from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from accounts.models import Accounts
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# For email verification code
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=email.split('@')[0]
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()
            #Email verification
            current_site=get_current_site(request)
            mail_subject='Plese verify your account'
            message=render_to_string('accounts/account_verification_mail.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_mail=email
            send_mail=EmailMessage(mail_subject,message, to=[to_mail])
            send_mail.send()
            # messages.success(request, 'Successfully registered, please check your mail')
            return redirect('/account/login/?command=verification&email='+email)    
    else:
        form=RegistrationForm()
    context={'form':form}

    return render (request, 'accounts/register.html',context)

def Login(request):
    if request.method =='POST':
        email=request.POST['Email']
        password=request.POST['Password']
        print(email, password)
        user=authenticate(email=email, password=password)
        # print(user)
        if user is not None :
            login(request,user)
            messages.success(request,'You are sucessfully logged in, will be redirected to dashboard')

            # print('success')
            return redirect ('dashboard')
        else:
            messages.error(request,'Invalid login credential')
            return redirect ('login')
    return render (request, 'accounts/login.html')

@login_required(login_url='login')
def Logout (request):
    logout(request)
    messages.success(request,'You are logged out')
    return redirect ('login')

def activate (request, uidb64, token):
    try:

        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)

    except (TypeError,ValueError, Accounts.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request,'You are verified successfully')
        return redirect ('login')
    else:
        messages.warning(request,'failed to verify')

        return redirect('register')

@login_required  
def dashboard (request):
    return render(request,'accounts/dashboard.html')


def forgetPassword (request):
    if request.method=='POST':
        email=request.POST['Email']
        if Accounts.objects.filter(email=email).exists():
            user=Accounts.objects.get(email__exact=email)
            #Email verification
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_mail=email
            send_mail=EmailMessage(mail_subject,message, to=[to_mail])
            send_mail.send()
            messages.success(request,'Reset password link has been sent to your email')
            return redirect ('login')
        else:
            messages.warning(request,'Account does not exist')

            return redirect('forgetPassword')

    return render(request,'accounts/forgetPassword.html')


def resetpassword_validate(request):
    return HttpResponse('done')





    

