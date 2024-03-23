from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from django.http import HttpResponse

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site

from .token import user_tokenizer_generate 

from django.template.loader import render_to_string #Setting up markup email verification links
from django.utils.encoding import force_bytes, force_str #Setting up markup email verification links
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode #decode token generator and it will useable and encode when sending it

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    
    form = CreateUserForm()
    
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        
        if form.is_valid():
            
            user = form.save() #Overwrite the account the user just registered into an instance
            
            user.is_active = False #Setting the user's account is deactivated 
            
            user.save() #Save all the accounts deactivated into database
            
            #Email verification setup (template)
            current_site = get_current_site(request)
            
            subject = 'Account verification email'
            #Collect all the parameters after the user registered account
            message = render_to_string('account/registration/email-verification.html',{
            
            
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), #encode the user id
                'token':user_tokenizer_generate.make_token(user),
            
            
            })
            
            user.email_user(subject=subject, message=message)
            
            return redirect('email-verification-sent') #Redirect to the verification link so the user can verify before using the account

    context = {
        'form': form,
    }
    
    return render(request, 'account/registration/register.html', context)


# Verify the email after user's clicked their verification link

def email_verification(request, uidb64, token):
    # Check the user's id and their token
    unique_id = force_str(urlsafe_base64_decode(uidb64)) #decode the user unique id
    
    user = User.objects.get(pk=unique_id)

    # Success / Activate the user's account after successful check if there are no issues
    
    if user and user_tokenizer_generate.check_token(user, token):
        
        user.is_active = True 
        user.save()
        
        return redirect('email-verification-success')
    
    #Failed / Keep the user's account deactivated and redirect to failed email verification template
    
    else:
        return redirect('email-verification-failed')




def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')



def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')

#Login

def my_login(request):
    
    form = LoginForm()
    
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
    
            if user is not None:
                
                auth.login(request, user)
                
                return redirect('dashboard')
            
            
    context ={
        'form': form,
    }
    
    return render(request, 'account/my-login.html',context=context)
    
#Logout
def user_logout(request):
    auth.logout(request)
    return redirect('store')

@login_required(login_url='my-login') #Gain access to the dashboard if only the user is logged in
def dashboard(request):
    
    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login') #Gain access to the profile_management if only the user is logged in
def profile_management(request):
    
    #Update user's username and email
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        
        user_form = UpdateUserForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            
            user_form.save()
            
            return redirect('dashboard')    
    
    
    context = {
        'user_form': user_form,
    }
    

    return render(request, 'account/profile-management.html', context=context)


@login_required(login_url='my-login') #Gain access to the profile_management if only the user is logged in
def delete_account(request):
    
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        
        user.delete()
        
        return redirect('store')
    
    return render(request, 'account/delete-account.html')