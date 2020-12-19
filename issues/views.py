from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Issue
from django.core.paginator import Paginator
from .forms import UserRegisterForm

# Create your views here.


def index(request):
    posts = Issue.objects.all().order_by('-date_posted')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
