from django.shortcuts import render, redirect

from django.views.generic import View
from scrum.models import *
from django.contrib.auth import authenticate, login
from forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

class AllPosts(LoginRequiredMixin, View):
	def get(self, request):
		order = request.GET.get('order', '-id')
		filter_ = request.GET.get('filter', 'id__gte=0')
		print filter_
		a, b = filter_.split('=')
		posts = Post.objects.filter(**{a:b}).order_by(order)
		return render(request, 'posts.html', {'posts': posts})

class ViewPost(LoginRequiredMixin, View):
	def get(self, request, id):
		post = Post.objects.get(id=int(id))
		return render(request, 'post.html', {'post': post, 'form': CommentForm()})

	def post(self, request, id):
		params = request.POST.copy()
		params.update({'author': request.user.id, 'parent': id})
		form = CommentForm(params)
		if form.is_valid():
			print "good"
			comment = form.save()
			return redirect(request.META['HTTP_REFERER'])
		return render(request, 'post.html', {'post': post, 'form': form})

class CreatePost(LoginRequiredMixin, View):
	def get(self, request):
		form = PostForm()
		return render(request, 'create_post.html', {'form': form})

	def post(self, request):
		params = request.POST.copy()
		params.update({'author': request.user.id})
		form = PostForm(params)
		if form.is_valid():
			post = form.save()
			return redirect(post.get_view_url())
		return render(request, 'create_post.html', {'form': form})

class Vote(LoginRequiredMixin, View):
	def post(self, request):
		post = request.POST['post']
		direction = request.POST['direction']
		Post.objects.get(id=post).set_vote(request.user, direction)
		return redirect(request.META['HTTP_REFERER'])

class SignUp(View):
	def get(self, request):
		form = ScrumUserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})

	def post(self, request):
		form = ScrumUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			if user is not None:
				user = authenticate(
					username=form.cleaned_data['username'],
					password=form.cleaned_data['password1']
				)
				login(request, user)
				return redirect('/')
		return render(request, 'registration/signup.html', {'form': form})
