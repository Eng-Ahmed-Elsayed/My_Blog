import os
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



from .models import User, Post, Category
from .forms import UserLoginForm, UserRegisterForm, ContactForm
# Create your views here.

def home(request):
    page_name = 'Home'
    authors = User.objects.filter(author=True)[:3]
    categories = Category.objects.all()
    # Create dict {category: his posts count, ....}
    categories_with_count = {}
    for category in categories:
        categories_with_count[category] = category.category_trend
    # Sort the dict
    categories_with_count = dict(sorted(categories_with_count.items(), key=lambda item: item[1], reverse=True))
    # Pick Top 15 categories
    categories_with_count = dict(list(categories_with_count.items())[:15])
    # Now we have top 15 categories with most posts
    categories = categories_with_count.keys()

    # We can get TRENDING POST and other posts with the same way (by comments).
    all_posts = Post.objects.all().order_by('-created')
    # Create dict {post: his_count, ....}
    posts_with_count = {}
    for post in all_posts:
        posts_with_count[post] = post.post_trend
    # Sort the dict
    posts_with_count = dict(sorted(posts_with_count.items(), key=lambda item: item[1], reverse=True))
    # Pick Top 15 posts and convert them to list
    posts_with_count = list(dict(list(posts_with_count.items())[:15]).keys())
    trending_post = posts_with_count[:3]
    # Will be updated after adding Favorite Class for users.
    popular_post = posts_with_count[0]
    # Random 3 posts
    you_may_like = all_posts.order_by('?')[:3]
    # Random pick Post
    editor_pick = all_posts.order_by('?')[0]
    
    oner = User.objects.get(id=1)

    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    context = {'categories': categories, 'posts': posts, 'editor_pick': editor_pick,
                'trending_post': trending_post, 'popular_post': popular_post,
                'you_may_like':you_may_like, 'oner': oner, 'authors': authors,
                'categories_with_count': categories_with_count, 'page_name': page_name}
    return render(request, 'base/home.html', context)

def error_page(request):
    page_name = '404'
    context = {'page_name': page_name}
    return render(request, 'base/404.html', context)
    

def login_user(request):
    page_name = 'Login'
    form = UserLoginForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        except:
            messages.error(request, "Username or password is not correct.")
    
        
    context = {'page_name': page_name, 'form': form}
    return render(request, 'base/login_register.html', context)

def register(request):
    page_name = 'Register'
    form = UserRegisterForm()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = user.password
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.username = user.username.lower()
                user.password = make_password(password)
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Those passwords didn’t match. Try again.')
        else:
            messages.error(request, form.errors.as_data())
    context = {'page_name': page_name, 'form': form}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')    
def logout_user(request):
    logout(request)
    return redirect('home')

def if_none_set_empty(field):
    if field == None:
        return ''
    return field

def search(request):
    try:
        # Get search content form request.get
        q = request.GET.get('q')
        username = request.GET.get('username')
        tag = request.GET.get('tag')
        category = request.GET.get('category')

        # Change page name to the search content
        d = dict(request.GET.lists())
        page_name = 'Search for '
        for v in [v for k, v in d.items()]:
            page_name += v[0] + ' & '
        page_name = page_name[:-2]
        # Normal Search with q
        if q != None:
            q = request.GET.get('q')
            posts = Post.objects.filter(
                Q(title__icontains=q)|
                Q(categories__name__icontains=q)|
                Q(tags__name=q)|
                Q(user__username__icontains=q)|
                Q(body__icontains=q)
            )

        # Search with username only
        elif username != None:
            posts = Post.objects.filter(Q(user__username=username))

        # Search with category only
        elif category != None:
            posts = Post.objects.filter(Q(categories__name=category))

        # Search with tag only
        elif tag != None:
            posts = Post.objects.filter(Q(tags__name=tag))

        # The search query content
        search_q = page_name[10:]

        # Ask if there is result or no
        if posts.exists() == False:
            page_name = 'Search Not Found'

        # Pagination working with search
        paginator = Paginator(posts, 4)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)    
        context = {'posts': posts, 'page_name': page_name, 'search_q': search_q}
        return render(request, 'base/search.html', context)
    except:
        return redirect('404')

@login_required(login_url='login')
def edit_profile(request):
    try:
        user = request.user
        if request.method == 'POST':
            # Edit Personal Information
            if 'changes' in request.POST:
                try:
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.phone = request.POST.get('phone')
                    user.bio = request.POST.get('bio')
                    user.job = request.POST.get('job')
                    if request.POST.get('avatar') != '':
                        old_img = user.avatar.path
                        try:
                            if old_img[-10:] != 'avatar.svg':
                                if os.path.exists(old_img):
                                    os.remove(old_img)
                                else:
                                    pass
                        except:
                            return redirect('404')
                        user.avatar = request.FILES['avatar']
                    user.save()
                    return redirect('edit_profile')
                except:
                    messages.error(request, 'Wrong Inputs')
            # Edit Password
            elif 'change_password' in request.POST:
                try:
                    old = request.POST.get('current_password')
                    if check_password(old, user.password):
                        if request.POST.get('new_password') == request.POST.get('confirm_password'):
                            user.set_password(request.POST.get('new_password'))
                            user.save()
                            logout(request)
                            login(request, user)
                            return redirect('home')
                        else:
                            messages.error(request, 'Wrong Password')
                    else:
                        messages.error(request, 'Wrong Password')
                except:
                    messages.error(request, '')
            # Edit Email Address
            elif 'change_email' in request.POST:
                try:
                    if user.email == request.POST.get('current_email'):
                        user.email = request.POST.get('new_email')
                        user.save()
                        return redirect('edit_profile')
                    messages.error(request, 'Wrong Email')
                except:
                    messages.error(request, 'Wrong Email')
            else:
                return redirect('404')
        context = {'user': user}    
        return render(request, 'base/edit_profile.html', context)
    except:
        return redirect('404')

def about_us(request):
    page_name = 'About Us'
    context = {'page_name': page_name}
    return render(request, 'base/about_us.html', context)

def contact(request):
    page_name = 'Contact Us'
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(request.path_info)
            # return redirect('about_us')
        else:
            messages.error(request, 'someting went wrong!!!')
    context = {'page_name': page_name, 'form': form}
    return render(request, 'base/contact.html', context)

def privacy_policy(request):
    page_name = 'Our Privacy Policy'
    context = {'page_name': page_name}
    return render(request, 'base/privacy_policy.html', context)

def terms_conditions(request):
    page_name = 'Our Terms And Conditions'
    context = {'page_name': page_name}
    return render(request, 'base/terms_conditions.html', context)