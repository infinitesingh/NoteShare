from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
        
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})



def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('note_list')
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password =  password)
        if user is not None:
            login(request, user)
            return redirect('note_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    
    else:
        return render(request, 'login.html')


def user_logout(r):
    logout(r)
    return redirect('login')

def note_list(r):
    notes = Note.objects.filter(author = r.user) 
    shared_notes = r.user.shared_notes.all()
    return render(r, 'note_list.html', {'notes':notes,'shared_notes':shared_notes })
    


@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note = Note.objects.create(title=title, content=content, author=request.user)
        return redirect('note_list')
    return render(request, 'note_form.html')

@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('note_list')
    return render(request, 'note_form.html', {'note': note})

@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

@login_required
def note_share(request, note_id):
    note = get_object_or_404(Note, id=note_id, author=request.user)
    users = User.objects.exclude(id = request.user.id)

    if request.method == 'POST':
        selected_users = request.POST.getlist('users')
        #username_to_share = request.POST.get('username')

        for user in users:
            if str(user.id) in selected_users:
                note.shared_with.add(user)
            else:
                note.shared_with.remove(user)
        
        return redirect('note_list')
    
        
        '''
        for user_id in selected_users:
            try:
                user_to_share = User.objects.get(id = user_id)
                note.shared_with.add(user_to_share)
            except User.DoesNotExist:
                return render(request, 'note_share.html', {'note': note, 'error': 'User not found'})
        return redirect('note_list')

        '''
    shared_users_ids = note.shared_with.values_list('id', flat=True)
    return render(request, 'note_share.html', {'note': note, 'users': users, 'shared_users_ids': shared_users_ids})

@login_required
def note_detail(r, note_id):
    note = get_object_or_404(Note, id = note_id)
    shared_users = note.shared_with.all()
    return render(r, 'note_detail.html', {'note': note, 'shared_users': shared_users})