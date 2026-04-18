from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'account/index.html')


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']


        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        messages.success(request, "Account created successfully!")
        return redirect('signin')


    return render(request, 'account/signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'account/index.html', {'fname': fname})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    

    return render(request, 'account/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully!")
    return redirect('home')
