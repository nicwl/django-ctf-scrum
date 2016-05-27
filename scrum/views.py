from django.shortcuts import render, redirect

from django.views.generic import View
from scrum.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from forms import *

class AllPosts(View):
	def get(self, request):
		return render(request, 'posts.html', {'posts': Post.objects.all()})

class ViewPost(View):
	def get(self, request, id):
		post = Post.objects.get(id=int(id))
		return render(request, 'post.html', {'post': post})

class CreatePost(View):
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


class Vote(View):
	def post(self, request):
		post = request.POST['post']
		direction = request.POST['direction']
		Post.objects.get(id=post).set_vote(request.user, direction)
		return redirect(request.META['HTTP_REFERER'])

class SignUp(View):
	def get(self, request):
		form = UserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})

	def post(self, request):
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			if user is not None:
				user = authenticate(
					username=form.cleaned_data['username'],
					password=form.cleaned_data['password1']
				)
				login(request, user)
				return redirect('/')
		return render(request, 'registration/signup.html', {'form': form})
