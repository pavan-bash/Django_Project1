from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import BlogFilter, CourseFilter
from django.db.models import F
import urllib.parse
from .forms import CommentForm, PublicCommentForm


def home(request):
	domains = Domain.objects.all()
	context = {'title': 'Home', 'domains': domains}
	return render(request, 'learning/home.html', context)

def about(request):
	comments = PublicComment.objects.all()
	no_of_comments = comments.count()
	form = PublicCommentForm()
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = PublicCommentForm(request.POST)
			if form.is_valid():
				new_form = form.save(commit=False)
				new_form.username = request.user
				new_form.save()
				return redirect("/about/")
		else:
			return redirect("/login/?next=/about/")
	context = {'title': 'About', 'comments': comments, "no_of_comments": no_of_comments, 'form': form}
	return render(request, 'learning/about.html', context)

def course(request, pk):
	domain = Domain.objects.get(id = pk)
	courses = Course.objects.filter(domain = domain)
	context = {'title': 'Home', 'courses': courses}
	return render(request, 'learning/course.html', context)

def all_courses(request):
	courses = Course.objects.all()
	myFilter = CourseFilter(request.GET, queryset=courses)
	courses = myFilter.qs
	context = {'title': 'All Courses', 'courses': courses, 'filter': myFilter}
	return render(request, 'learning/all_courses.html', context)

@login_required
def enroll(request, pk):
	course = Course.objects.get(id = pk)
	if request.method == 'POST':
		hold = Enrollment.objects.filter(username=request.user, coursename=course).count()
		if hold:
			messages.warning(request, f'You have already enrolled for the course {course.name}')
		else:
			Enrollment.objects.create(username=request.user, coursename=course)
			messages.success(request, f'You have enrolled for the course {course.name}')
		return redirect('dashboard')
	context = {'title': 'Enroll', 'course': course}
	return render(request, 'learning/enroll.html', context)

@login_required
def delete_course(request, pk):
	course = Course.objects.get(id = pk)
	if request.method == 'POST':
		Enrollment.objects.filter(username=request.user, coursename=course).delete()
		messages.success(request, f'You have exited form the course {course.name}')
		return redirect('dashboard')
	context = {'title': 'Delete Course', 'course': course}
	return render(request, 'learning/delete_course.html', context)

@login_required
def dashboard(request):
	enrolls = Enrollment.objects.filter(username=request.user)
	blogposts = Post.objects.filter(author=request.user)
	context = {'title': 'Dashboard', 'enrolls': enrolls, 'blogposts': blogposts}
	return render(request, 'learning/dashboard.html', context)	

def blog(request):
	posts = Post.objects.all()
	context = {'title': 'Blog', 'posts': posts}
	return render(request, 'learning/blog.html', context)


@login_required
def content(request, pk):
	context = {'title': 'Dashboard'}
	s = ""
	pk = pk.lower()
	for _ in pk.split():
		s += _
	return render(request, 'learning/courses/'+s+'.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'learning/blog.html'	
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		return BlogFilter(self.request.GET, queryset=self.model.objects.all()).qs.order_by('-date_posted')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		context['filter'] = BlogFilter(self.request.GET, queryset=self.model.objects.all())
		return context

class UserPostListView(ListView):
	model = Post
	template_name = 'learning/user_post.html'	
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		context['filter'] = BlogFilter(self.request.GET, queryset=self.model.objects.all())
		return context

def blog_detail(request, pk):
	post = Post.objects.get(id=pk)
	share_string = urllib.parse.quote_plus(post.content)
	no_of_likes = Like.objects.filter(postname=post).count()
	comments = Comment.objects.filter(postname=post)
	form = CommentForm()
	if request.method == 'POST':
		if request.user.is_authenticated:
			hold = Like.objects.filter(username=request.user, postname=post).count()
			form = CommentForm(request.POST)
			if form.is_valid():
				new_form = form.save(commit=False)
				new_form.username = request.user
				new_form.postname = post
				new_form.save()
				return redirect("/blog/"+pk+"/")
			else:
				print("HI")
				form = CommentForm()
			if hold:
				messages.warning(request, f'You have already liked this post!')
			else:
				Like.objects.create(username=request.user, postname=post)
			return redirect("/blog/"+pk+"/")
		else:
			return redirect("/login/?next=/blog/"+pk+"/")

	context = {
		'title': 'Blog', 
		'share_string': share_string, 
		'post': post, 
		'no_of_likes': no_of_likes,
		'comments': comments,
		'form': form,
	}
	return render(request, 'learning/post_detail.html', context)

def login_to_comment(request, pk):
	return redirect("/login/?next=/blog/"+pk+"/")

def login_to_commentpublic(request):
	return redirect("/login/?next=/about/")

class PostDetailView(DetailView):
	model = Post
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		context['share_string'] = urllib.parse.quote_plus(context['content'])
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'category', 'This_blog_is_about', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/blog'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Blog'
		return context

	