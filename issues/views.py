from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import UserProfile, Issue, Comment, DisLike, Like
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from .forms import UserRegisterForm, CommentForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    issues = Issue.objects.all().order_by('-date_posted')
    paginator = Paginator(issues, 10)
    page = request.GET.get('page')
    issues = paginator.get_page(page)
    return render(request, 'index.html', {'issues': issues})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, f'User {user} Created Sucessfully! Now Login')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)


class UserListView(ListView):
    model = Issue
    template_name = 'user_posts.html'
    context_object_name = 'issues'
    ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Issue.objects.filter(user=user).order_by('-date_posted')


class IssueDetailView(DetailView):
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        messages.success(self.request, f'Issue with title {title} Created!')
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.user:
            return True
        return False

    def get_success_url(self):
        return reverse('index')


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/'

    def test_func(self):
        Issue = self.get_object()
        if self.request.user == Issue.user:
            return True
        return False


def searchissue(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(context__icontains=query)
            results = Issue.objects.filter(lookups).distinct()
            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Issue, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = post
            comment.user = request.user
            comment.save()
            return redirect('issue-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})



class Requirement(View):
    form_class = CommentForm
    template_name = 'tcomment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        comment = Comment.objects.all()
        context = {}
        context['page_obj'] = comment
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = request.user
            comment_form.save()
            messages.success(request, 'Your comment successfully addedd')

            return reverse('comment')
        
        context = {}
        context['form'] = form

        return render(request, self.template_name, context)
      
      
class UpdateCommentVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):

        comment_id = self.kwargs.get('comment_id', None)
        opition = self.kwargs.get('opition', None) # like or dislike button clicked

        comment = get_object_or_404(Comment, id=comment_id)
        pk = comment.issue.id

        try:
            # If child DisLike model doesnot exit then create
            comment.dis_likes
        except Comment.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment = comment)

        try:
            # If child Like model doesnot exit then create
            comment.likes
        except Comment.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(comment = comment)

        if opition.lower() == 'like':

            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:    
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:    
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)
        else:
            return redirect('issue-detail', pk=pk)
        return redirect('issue-detail', pk=pk)