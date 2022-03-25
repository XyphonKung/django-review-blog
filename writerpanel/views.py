from django.shortcuts import render,redirect
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Create your views here.
@login_required(login_url='member')
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    return render(request, 'backend/index.html',{'blogs':blogs,'writer':writer,'blogCount':blogCount,'total':total})

@login_required(login_url='member')
def displayFrom(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()
    return render(request, 'backend/blogFrom.html',{'blogs':blogs,'writer':writer,'blogCount':blogCount,'total':total,'categories':categories})

@login_required(login_url='member')
def insertData(request):
    try:
        if request.method == 'POST' and request.FILES['image']:
            dataFile = request.FILES['image']
            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']
            content = request.POST['content']
            writer = auth.get_user(request)

            if str(dataFile.content_type).startswith('image'):
                #upload
                fs = FileSystemStorage()
                img_url = 'blogsImages/'+dataFile.name
                filename = fs.save(img_url,dataFile)
                #save data
                blog = Blogs(name=name,category_id=category,description=description,content=content,writer=writer,image=img_url)
                blog.save()
                messages.info(request,"บันทึกข้อมูลเรียบร้อย")

                return redirect('displayFrom')
            else:
                messages.info(request,"ไฟล์ที่อัพโหลดไม่รองรับ กรุณาอัพโหลดไฟล์รูปภาพอีกครั้ง")
                return redirect('displayFrom')
    except:
        return redirect('displayFrom')

@login_required(login_url='member')
def deleteData(request,id):
    try:
        blog=Blogs.objects.get(id=id)
        fs=FileSystemStorage()
        fs.delete(str(blog.image))
        blog.delete()
        return redirect('panel')
    except:
        return redirect('panel')

@login_required(login_url='member')
def editData(request,id):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()

    blogEdit=Blogs.objects.get(id=id)
    return render(request, 'backend/editForm.html',{'blogEdit':blogEdit,'writer':writer,'blogCount':blogCount,'total':total,'categories':categories})

@login_required(login_url='member')
def updateData(request,id):
    try:
        if request.method == 'POST' :
            #Query olg blog data
            blog=Blogs.objects.get(id=id)

            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']
            content = request.POST['content']

            #update data
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()

            #update image
            if request.FILES['image']:
                dataFile = request.FILES['image']
                if str(dataFile.content_type).startswith('image'):
                    #delete old image
                    fs = FileSystemStorage()
                    fs.delete(str(blog.image))
                    #replace with new image
                    img_url = 'blogsImages/'+dataFile.name
                    filename = fs.save(img_url,dataFile)
                    blog.image = img_url
                    blog.save()
        return redirect('panel')
    except :
        return redirect('panel')
        