from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import ForumRoomForm, TopicForm
from .models import ForumRoom, Message, Topic
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated: 
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
    
    context = {'page': page}
            
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('index')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            User.save(user)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = ForumRoom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(creator__username__icontains=q)   
    )
    
    topics = Topic.objects.all()[:5]
    roomMessages = Message.objects.all()[:5]
    context = {'rooms': rooms, 'roomMessages': roomMessages, 'topics': topics}
    return render(request, 'base/home.html', context)

@login_required(login_url='loginPage')
def roomPage(request, pk):
    
    room = ForumRoom.objects.get(id=pk)
    roomMessages = room.message_set.all().order_by('created_at')
    participiants = room.participiants.all()
    
    topics = Topic.objects.all()[:5]
    
    if request.method == 'POST':
        message = Message.objects.create(body=request.POST.get('body'), user=request.user, room=room)
        room.participiants.add(request.user)
        return redirect('roomPage', pk=room.id)
    
    context = {'room': room, 'roomMessages': roomMessages , 'participiants': participiants, 'topics':topics}
    return render(request, 'base/room_page.html', context)

@login_required(login_url='loginPage')
def createRoom(request):
    form = ForumRoomForm()
    if request.method == 'POST':
        form = ForumRoomForm(request.POST)
        if form.is_valid() and not ForumRoom.objects.filter(name=request.POST.get('name')).exists():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            return redirect('index')
        else:
            messages.error(request, 'This room name already exists!')
            
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='loginPage')
def deleteRoom(request, pk):
    room = ForumRoom.objects.get(id=pk)
    if request.user != room.creator:
        return redirect('index')    
    ForumRoom.objects.get(id=pk).delete()
    return redirect('index')
        
@login_required(login_url='loginPage')
def profilePage(request, pk):
    topics = Topic.objects.all()[:5]
    user = User.objects.get(id=pk)  
    rooms = ForumRoom.objects.filter(creator=user);
    roomMessages = Message.objects.filter(user=user).order_by('created_at')[:5]
    context={'user': user, 'rooms': rooms, 'roomMessages': roomMessages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='loginPage')
def createTopic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request, 'This Topic name already exists!')
           
    return render(request, 'base/topic_form.html', {'form': form})