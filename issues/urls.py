from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('issue/<int:pk>/', views.IssueDetailView.as_view(), name='issue-detail'),
    path('issue/new/', views.IssueCreateView.as_view(), name='issue-create'),
    path('issue/<int:pk>/update/', views.IssueUpdateView.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete/', views.IssueDeleteView.as_view(), name='issue-delete'),
    path('user/<str:username>/', views.UserListView.as_view(), name='user-issues'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('profile/', views.view_profile, name='view_profile'),
    path('requirement/<int:comment_id>/<str:opition>/', views.UpdateCommentVote.as_view(), name='requirement_comment_vote'),
    path('irequirement/<int:issue_id>/<str:opition>/', views.UpdateIssueVote.as_view(), name='requirement_issue_vote'),
]
