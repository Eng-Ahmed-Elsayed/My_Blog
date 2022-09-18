from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from base.models import Post, User
# Create your views here.

def author_profile(request, pk):
    try:
        author = get_object_or_404(User, pk=pk)
        if author.author == True:
            page_name = author.fullname
            posts = Post.objects.filter(user=author)
            paginator = Paginator(posts, 3)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {'posts': posts, 'author': author, 'page_name': page_name}
            return render(request, 'authors/author.html', context)
        else:
            return redirect('404')
    except:
        return redirect('404')

def authors(request):
    try:
        authors = User.objects.filter(author=True)
        page_name = 'Authors'
        context = {'authors': authors, 'page_name': page_name}
        return render(request, 'authors/authors.html', context)
        
    except:
        return redirect('404')