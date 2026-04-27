from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from AuthSystem import settings
from django.core.mail import send_mail

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

        if User.objects.filter(username=username):
            messages.error(request, 'User name already exist; Please try another username!')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, 'Email is already exist, Please use some other email!')
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('home')
        
        if password != confirm_password:
            messages.error(request, "Password didn't match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, 'Username must be Alpha numeric')
            return redirect('home')
        

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        messages.success(request, "Account created successfully!")

        # Welcome Email
        subject = "Welcome to AuthSystem"

        message = (
            f"Hello {myuser.first_name}!!\n\n"
            "Welcome to AuthSystem!\n"
            "Thank you for visiting the website.\n"
            "We have also received your confirmation email address in order to activate your account.\n\n"
            "Thank you,\n"
            "Sonu Gupta"
        )

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

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
