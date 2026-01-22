from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Blocklist
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve


# Create your views here.
class AboutView(TemplateView):
    template_name = "basic_app/about.html"


class PostList(ListView):
    model = Post
    name = "Posts"

    def get_queryset(self):
        return Post.objects.filter(is_Published=True).order_by("-publication_date")

    context_object_name = "posts"


class DraftList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Post
    extra_context = {"isDrafts": True}

    def get_queryset(self):
        return Post.objects.filter(
            is_Published=False, author=self.request.user
        ).order_by("-creation_date")

    context_object_name = "posts"


class PostDetail(DetailView):
    model = Post
    extra_context = {"commentAllowed": False}

    def get(self, request, *args, **kwargs):
        result = super().get(self, request, *args, **kwargs)
        if request.user.is_authenticated:
            blocked = Blocklist.objects.filter(post=self.object, user=self.request.user)
            if blocked:
                self.extra_context["commentAllowed"] = False
            else:
                self.extra_context["commentAllowed"] = True

        if self.object.author == request.user or self.object.is_Published:
            return result
        else:
            return redirect("/")


def postDetail(request, pk):
    object = get_object_or_404(Post, pk=pk)
    return render(
        request, "basic_app/post_detail.html", {"post": object, "form": CommentForm()}
    )


class CreatePost(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "postlist"
    model = Post
    form_class = PostForm

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "postlist"
    model = Post
    form_class = PostForm

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return self.request.user == post.author


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "postlist"
    success_url = "/"
    model = Post

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return self.request.user == post.author


#################################################


# class CreateComment(CreateView):
#     model = Comment
#     form_class = CommentForm
#     def form_valid(self, form):
#         pk = self.kwargs.get("pk")
#         post = get_object_or_404(Post, pk=pk)
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.user=request.user
#         comment.save()
#         return super().form_valid(form)


def checkBan(request, post):
    blocklist = post.blocklist_set.filter(user=request.user)

    if blocklist:
        return True
    else:
        return False


def banUser(request, userpk, postpk):
    user = get_object_or_404(User, pk=userpk)
    post = get_object_or_404(Post, pk=postpk)
    block = Blocklist.objects.get_or_create(user=user, post=post)
    if not block[1]:
        block[0].delete()
    return redirect("blog:detail", pk=postpk)


def createComment(request, pk):
    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            comment = form.save(commit=False)
            if checkBan(request, post):
                return redirect("blog:detail", pk=post.pk)

            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect("blog:detail", pk=post.pk)
    form = CommentForm()
    return render(request, "basic_app/comment_form.html", {"form": form})


@login_required
def commentApprove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.post.author:
        comment.approve()
        return redirect("blog:detail", pk=comment.post.pk)


@login_required
def postPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.publish()
        return redirect("blog:detail", pk=post.pk)


@login_required
def commentRemove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("blog:detail", pk=post_pk)


class ListComment(ListView):
    model = Comment
    template_name = "basic_app/post_list"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(Post, pk=pk)
        return Comment.objects.filter(post=post, approved=True).order_by(
            "creation_date"
        )
