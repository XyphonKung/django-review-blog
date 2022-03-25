from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    latest = Blogs.objects.all().order_by('-pk')[:4]

    #popular blog
    popular =  Blogs.objects.all().order_by('-views')[:3]
    #recommend blog
    recblog =  Blogs.objects.all().order_by('views')[:3]

    #pagination
    paginator = Paginator(blogs,3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        blogPerpage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)
    
    return render(request,'frontend/index.html',{
                                                'categories':categories,
                                                'blogs':blogPerpage,
                                                'latest':latest,
                                                'popular':popular,
                                                'recblog':recblog
                                                })

def BlogDetail(request,id):
    categories = Category.objects.all()
    #popular blog
    popular =  Blogs.objects.all().order_by('-views')[:3]
    #recommend blog
    recblog =  Blogs.objects.all().order_by('views')[:3]

    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views+1
    singleBlog.save()
    return render(request,"frontend/blogDetail.html",{'categories':categories,
                                                        'blog':singleBlog,
                                                        'popular':popular,
                                                        'recblog':recblog
                                                    })
def searchCategory(request,category_id):
    categories = Category.objects.all()
    #popular blog
    popular =  Blogs.objects.all().order_by('-views')[:3]
    #recommend blog
    recblog =  Blogs.objects.all().order_by('views')[:3]
    categoryName =  Category.objects.get(id=category_id)

    blogs = Blogs.objects.filter(category_id=category_id)
    return render(request,"frontend/searchCategory.html",{'blogs':blogs,
                                                        'popular':popular,
                                                        'recblog':recblog,
                                                        'categoryName':categoryName,
                                                        'categories':categories
                                                        })
def searchWriter(request,writer):
    categories = Category.objects.all()
    #popular blog
    popular =  Blogs.objects.all().order_by('-views')[:3]
    #recommend blog
    recblog =  Blogs.objects.all().order_by('views')[:3]

    blogs = Blogs.objects.filter(writer=writer)
    return render(request,"frontend/searchWriter.html",{'blogs':blogs,
                                                        'popular':popular,
                                                        'recblog':recblog,                                                       
                                                        'categories':categories,
                                                        'writer':writer
                                                        })
