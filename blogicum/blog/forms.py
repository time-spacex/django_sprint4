from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Класс для создания формы публикации."""

    class Meta:

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Классс для создания формы комментария к публикации."""

    class Meta:
        model = Comment
        fields = ('text',)
