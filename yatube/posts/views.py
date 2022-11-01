from .forms import PostForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Post, Group, User
from .utils import pagination


def index(request):
    post_list = Post.objects.all()
    page_obj = pagination(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts_of_group.all()
    page_obj = pagination(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    users_post = author.author_of_posts.all()
    post_count = users_post.count()
    page_obj = pagination(request, users_post)
    context = {
        'context': author,
        'page_obj': page_obj,
        'post_count': post_count,
        'users_post': users_post,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, id=post_id)
    author_posts = post.author.author_of_posts.count()
    context = {
        'post': post,
        'author_posts': author_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    author = request.user
    is_edit = True
    if author != post.author:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        return render(
            request,
            template,
            context={'form': form, 'post': post}
        )
    form = PostForm()
    context = {
        'context': author,
        'is_edit': is_edit,
        'form': form,
        'post': post
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    author = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            post.save()
            return redirect('posts:profile', author)
        return render(request, template, context={'form': form})
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, template, context)
