from django import forms
from models import *
from django.contrib.auth.forms import UserCreationForm
import unicodedata

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'title', 'url', 'text']
		widgets = {
			'title': forms.TextInput
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['author', 'parent', 'text']
		widgets = {
			'parent': forms.HiddenInput
		}

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))

class ScrumUserCreationForm(UserCreationForm):
	class Meta:
		model = ScrumUser
		fields = ("username",)
        field_classes = {'username': UsernameField}