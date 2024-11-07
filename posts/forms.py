from django import forms 
from .models import  Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {  # corrected from 'widget' to 'widgets'
            'image': forms.ClearableFileInput()
        }
        



class CommentForm(forms.ModelForm):
    class Meta:
        model =  Comment
        fields = ['comment']


