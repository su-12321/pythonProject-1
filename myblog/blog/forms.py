"""
表单定义
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category, Tag

class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    email = forms.EmailField(required=True, label='邮箱')
    first_name = forms.CharField(max_length=30, required=False, label='名')
    last_name = forms.CharField(max_length=30, required=False, label='姓')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """用户资料表单"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': '名',
            'last_name': '姓',
            'email': '邮箱',
        }

class PostForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'summary', 'category', 'tags',
                 'cover_image', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '标题',
            'content': '内容',
            'summary': '摘要',
            'category': '分类',
            'tags': '标签',
            'cover_image': '封面图片',
            'status': '状态',
            'is_featured': '设为推荐',
        }

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '写下你的评论...'
            }),
        }
        labels = {
            'content': '评论',
        }

class CategoryForm(forms.ModelForm):
    """分类表单"""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TagForm(forms.ModelForm):
    """标签表单"""
    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
