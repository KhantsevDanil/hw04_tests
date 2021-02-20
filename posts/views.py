from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'posts/index.html',
        {'page': page, "paginator": paginator, "post_list": post_list},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all().order_by('-pub_date')
    post_list = posts
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "group.html",
        {'page': page, 'group': group, "paginator": paginator}
    )


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:index'))
        return render(request, 'posts/new_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/profile.html', {'author': author,
                                                  'page': page,
                                                  'paginator': paginator
                                                  })


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    author = get_object_or_404(User, username=username)
    return render(request,
                  'posts/post.html',
                  {'post': post, 'author': author}
                  )


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    item = get_object_or_404(Post, author=author, id=post_id)
    if request.user != author:
        redirect(reverse(
            "posts:post_view", args=[author.username, post_id]))
    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect(reverse(
            "posts:post_view", args=[author.username, post_id]))
    return render(request,
                  'posts/new_post.html',
                  {"form": form, "item": item})
