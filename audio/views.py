from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from audio.models import Music

login_required(login_required('login'))
def index(request):
    music = Music.objects.all()
    return render(request, 'index.html', {'music': music})

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password is Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


login_required(login_required('login'))
def logout(request):
    auth.logout(request)
    return redirect('login')



@login_required(login_url='login')
def music(request, pk):
    movie_detail = get_object_or_404(Music, id=pk)
    context = {
        'music': movie_detail
    }
    return render(request, 'music.html', context)

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        music = Music.objects.filter(title__icontains=search_query)
        context = {
            'music': music,
            'search_query': search_query,
            'search_results_count': len(music)
        }
    else:
        context = {}

    return render(request, 'search.html', context)