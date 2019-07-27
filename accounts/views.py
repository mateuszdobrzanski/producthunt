from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def is_blank(text):
    # If text is blank OR empty return false
    if text and text.strip():
        return False
    return True


def signup(request):
    if request.method == 'POST':
        # The has info and wants signup

        if is_blank(request.POST['username']):
            return render(request, 'accounts/signup.html', {'error': 'Username cannot be blank.'})

        if is_blank(request.POST['password']):
            return render(request, 'accounts/signup.html', {'error': 'Password cannot be blank.'})

        if request.POST['password'] == request.POST['passwordConfirmation']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already taken'})

            except User.DoesNotExist:
                if not is_blank(request.POST['email']):
                    user = User.objects.create_user(username=request.POST['username'],
                                                    email=request.POST['email'],
                                                    password=request.POST['password'])
                    auth.login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'accounts/signup.html', {'error': 'Email cannot be blank.'})
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password are not same.'})
    else:
        # user wants to enter info
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Login or user is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


@login_required(login_url="/accounts/login")
def account_detail(request):
    return render(request, 'accounts/account.html')
