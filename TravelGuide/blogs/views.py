from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from reportlab.pdfbase.pdfdoc import count

from .models import Blog, Upvote, Comment

def create_blog(request):
    if request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        img = request.POST['img']
        flair = request.POST['flair']

        Blog.objects.create(title=title, flair=flair,poster=request.user,body=body,blog_img=img)
        return redirect('/blogs/')
    return render(request,'blog.html')

def upvote(request):
    blog = Blog.objects.get(pk=2)
    Upvote.objects.create(user=request.user,blog=blog)
    like = Upvote.objects.filter(blog=blog).count()
    comment = Comment.objects.filter(blog=blog).count()
    comments = Comment.objects.filter(blog=blog).all()
    return render(request,'blog-edu-single.html',{'blog':blog,'like':like,'comment':comment,'comments':comments})

def blog_single(request):
    blog = Blog.objects.get(pk=1)
    like = Upvote.objects.filter(blog=blog).count()
    comment = Comment.objects.filter(blog=blog).count()
    comments = Comment.objects.filter(blog=blog).all()
    if request.method == "POST":
        body = request.POST['body']
        Comment.objects.create(blog=blog,user=request.user,body=body)
        return redirect('/blogs/see/1/')
    return render(request,'blog-edu-single.html',{'blog':blog,'like':like,'comment':comment,'comments':comments})


def blog_more(request):
    blog = Blog.objects.get(pk=2)
    like = Upvote.objects.filter(blog=blog).count()
    comment = Comment.objects.filter(blog=blog).count()
    comments = Comment.objects.filter(blog=blog).all()
    if request.method == "POST":
        body = request.POST['body']
        Comment.objects.create(blog=blog, user=request.user, body=body)
        return redirect('/blogs/see/2/')
    return render(request, 'blog-edu-single.html',
                  {'blog': blog, 'like': like, 'comment': comment, 'comments': comments})


def blog_single3(request):
    blog = Blog.objects.get(pk=3)
    return render(request,'blog-edu-single.html',{'blog':blog})



def all_blogs(request):
    blogs = Blog.objects.all()
    upvotes = Upvote.objects.all()
    comments = Comment.objects.all()
    return render(request,'blogs.html',{'blogs':blogs,'upvotes':upvotes,'comments':comments})
