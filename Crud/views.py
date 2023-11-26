from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student


def home(request):
    data = Student.objects.all()
    # Retrieve messages and pass them to the template context
    stored_messages = messages.get_messages(request)
    return render(request, 'index.html', {'data': data, 'messages': stored_messages})


def insertData(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        hifadhi = Student(name=name, email=email, age=age, gender=gender)

        hifadhi.save()
        return redirect('/')
    else:
        return render(request, 'index.html')


def updateData(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        rekebisha = Student.objects.get(id=id)
        rekebisha.name = name
        rekebisha.email = email
        rekebisha.age = age
        rekebisha.gender = gender

        rekebisha.save()
        return redirect('/')
    else:
        d = Student.objects.get(id=id)
        return render(request, 'edit.html', {'d': d})


def delete(request, id):
    d = Student.objects.get(id=id)
    d.delete()
    return redirect('/')


def handlesignup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Sorry. Unfortunately this username is already taken. Please input a different one.')
                return render(request, 'signup.html', {'messages': messages.get_messages(request)})
            myuser = User.objects.create_user(username, password)
            myuser.save()
            messages.success(request, 'Congratulations our esteemed customer! You have successfully created your Salama Millers customer account! Welcome!')
            return redirect('handlelogin')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})
    return render(request, 'signup.html')


def handlelogin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        myuser = authenticate(username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, 'Congratulations our esteemed customer! You have successfully logged into your Salama Millers customer account! Make your orders here. Welcome!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('/login')
    return render(request, 'login.html')


def handlelogout(request):
    logout(request)
    return render(request, 'login.html')
