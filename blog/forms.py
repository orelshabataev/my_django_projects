from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, empty_label='Выберите категорию', label='Категория')

    class Meta:
        model = Post
        fields = ['title', 'is_published', 'content', 'photo', 'slug', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-input'})
        }

