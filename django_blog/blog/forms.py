from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # The author field is explicitly excluded, as it will be set automatically 
        # in the CreateView based on the logged-in user.
        fields = ['title', 'content'] 
        # Optional: Add widgets for styling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here...'})
    )

    class Meta:
        model = Comment
        fields = ['content']
