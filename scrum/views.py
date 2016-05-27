from django.shortcuts import render, redirect

from django.views.generic import View
from scrum.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

class AllPosts(View):
	def get(self, request):
		return render(request, 'posts.html', {'posts': [{'title': 'No link', 'id': 0}, {'title': 'Link', 'url': 'http://www.google.com', 'id': 1}]})

class Vote(View):
	def post(self, request):
		post = request.POST['post']
		direction = request.POST['direction']
		Post.objects.get(id=post).vote(request.user, direction)
		return redirect(request.META['HTTP_REFERER'])

class SignUp(View):
	def get(self, request):
		form = UserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})

	def post(self, request):
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				user = authenticate(
					username=form.cleaned_data['username'],
					password=form.cleaned_data['password1']
				)
				login(request, user)
				return redirect('/')
		return render(request, 'registration/signup.html', {'form': form})
