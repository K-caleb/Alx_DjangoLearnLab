from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Registration error. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Login failed. Please check your username and password.")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        email = request.POST.get("email")
        if email:
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Email cannot be empty.")
    return render(request, "blog/profile.html")

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

# Import the new models and forms
from .models import Post, Comment
from .forms import PostForm, CommentForm
# ... existing forms/views imports (CustomUserCreationForm, UserEditForm, register, profile) ... 

# --- R: Detail View (Update to include the CommentForm) ---
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    # Override get_context_data to pass the CommentForm to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass an empty comment form for new submissions
        context['comment_form'] = CommentForm() 
        return context

# --- C: Create Comment View (Function-Based for simplicity) ---
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 1. Create the comment object but don't save to database yet
            comment = form.save(commit=False)
            # 2. Attach the post and the logged-in user
            comment.post = post
            comment.author = request.user
            # 3. Save to database
            comment.save()
            messages.success(request, 'Your comment was posted successfully.')
            # Redirect back to the post detail page
            return HttpResponseRedirect(post.get_absolute_url()) 
        else:
            # If form is invalid, redirect back to post detail with error message
            messages.error(request, 'Error posting comment. Please check your input.')
    
    # If not POST or if form was invalid but we want to display the error context
    return HttpResponseRedirect(post.get_absolute_url())


# --- U: Update Comment View (Login Required & Ownership Check) ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    # Redirect back to the post detail view upon success
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
        
    # Check if the user trying to update the comment is the author
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# --- D: Delete Comment View (Login Required & Ownership Check) ---
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    # Redirect back to the post detail view upon success
    def get_success_url(self):
        post_pk = self.object.post.pk
        messages.warning(self.request, 'Comment deleted successfully.')
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})

    # Check if the user trying to delete the comment is the author
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
