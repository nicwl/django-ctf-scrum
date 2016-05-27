from django import forms
from models import *

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'title', 'url', 'text']
		widgets = {
			'title': forms.TextInput
		}
