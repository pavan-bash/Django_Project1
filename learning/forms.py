from django import forms
from .models import Comment, PublicComment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

class PublicCommentForm(forms.ModelForm):
	class Meta:
		model = PublicComment
		fields = ['content']
