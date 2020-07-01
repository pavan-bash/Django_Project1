from django.urls import path, include
from . import views
from learning.views import (
	PostListView, 
	PostDetailView, 
	PostCreateView, 
	PostUpdateView,
	PostDeleteView,
    UserPostListView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('course/<str:pk>', views.course, name="course"),
    path('all_courses/', views.all_courses, name="all_courses"),
    path('enroll/<str:pk>', views.enroll, name="enroll"),
    path('delete_course/<str:pk>', views.delete_course, name="delete_course"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:pk>/', views.content, name='content'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('blog/new/', PostCreateView.as_view(), name='blog-create'),
    path('blog/<str:pk>/', views.blog_detail, name='blog_detail'),
    path('login_to_comment/<str:pk>/', views.login_to_comment, name='login_to_comment'),
    path('login_to_comment/', views.login_to_commentpublic, name='login_to_commentpublic'),
    path('blog/<str:pk>/update', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<str:pk>/delete', PostDeleteView.as_view(), name='blog-delete'),
    path('blog/user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('ip/', views.ipview, name = 'ipview'),
]