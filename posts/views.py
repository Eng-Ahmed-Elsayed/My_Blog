from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from base.models import Post, Comment
from .forms import PostForm, CommentForm
# Create your views here.

def recent_posts(request):
    page_name = 'RECENT POSTS'
    posts = Post.objects.all().order_by('-created')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    context = {'posts': posts, 'page_name': page_name}
    return render(request, 'posts/posts.html', context)

def trending_posts(request):
    page_name = 'TRENDING POSTS'
    posts = Post.objects.all().order_by('-created')
    # Create dict {post: his_count, ....}
    posts_with_count = {}
    for post in posts:
        posts_with_count[post] = post.post_trend
    # Sort the dict
    posts_with_count = dict(sorted(posts_with_count.items(), key=lambda item: item[1], reverse=True))
    posts_with_count = list(dict(list(posts_with_count.items())).keys())
    paginator = Paginator(posts_with_count, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    context = {'posts': posts, 'page_name': page_name}
    return render(request, 'posts/posts.html', context)

@login_required(login_url='login')
def create_post(request):
    user = request.user
    page_name = 'Create Post'
    if (user.is_staff and user.author == True) or user.is_superuser:
        form = PostForm()
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()
                pk = post.id
                return redirect('post_details', pk=pk)
            else:
                messages.error(request, form.errors.as_data())
        context = {'form': form, 'page_name': page_name}
        return render(request, 'posts/create_and_update_post.html', context)
    else:
        return redirect('404')

@login_required(login_url='login')
def update_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    page_name = 'Update Post'
    if user.is_superuser or post.user == user:
        form = PostForm(instance=post)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                return redirect('post_details', pk=pk)
            else:
                messages.error(request, form.errors.as_data())
                
        context = {'form': form, 'page_name': page_name}
        return render(request, 'posts/create_and_update_post.html', context)
    else:
        return redirect('404')


def post_details(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        page_name = post.title
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('created')
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment_field = form.cleaned_data['comment_field']
                user = request.user
                comment = Comment(user=user, comment_field=comment_field, post=post)
                comment.save()
                return redirect('post_details', pk=pk)
        context = {'post': post, 'page_name': page_name, 'form': form, 'comments':comments}
        return render(request, 'posts/post_details.html', context)
    except:
        return redirect('404')