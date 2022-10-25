from .forms import PostForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Post, Group, User


AMOUNT_POSTS_ON_PAGE = 2


@login_required
def index(request):
    post_list = Post.objects.all()
    # В словаре context отправляем информацию в шаблон
    paginator = Paginator(post_list, AMOUNT_POSTS_ON_PAGE)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts_of_group.all()
    paginator = Paginator(post_list, AMOUNT_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    users_post = Post.objects.filter(author=user)
    post_count = users_post.count()
    paginator = Paginator(users_post, AMOUNT_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'post_count': post_count,
        'users_post': users_post,
    }
    return render(request, 'posts/profile.html', context)


@login_required
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
    user = request.user
    is_edit = True
    if user != post.author:
        return redirect('posts:post_detail', post_id)
    else:
        if request.method == 'POST':
            form = PostForm(request.POST or None)
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.group = form.cleaned_data['group']
                post.save()
                return redirect('posts:profile', user)
            return render(
                request,
                template,
                context={'form': form, 'post': post}
            )
        form = PostForm()
        context = {
            'user': user,
            'is_edit': is_edit,
            'form': form,
            'post': post,
            'groups': Group.objects.all(),
        }
        return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.group = form.cleaned_data['group']
            post.save()
            return redirect('posts:profile', user)
        return render(request, template, context={'form': form})
    form = PostForm()
    context = {
        'form': form,
        'groups': Group.objects.all(),
    }
    return render(request, template, context)
