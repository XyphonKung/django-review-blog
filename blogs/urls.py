from django.urls import path
from .views import index,BlogDetail,searchCategory,searchWriter
urlpatterns = [
    path('', index),
    path('blog/<int:id>',BlogDetail,name="blogDetail"),
    path('blog/category/<int:category_id>',searchCategory,name="searchCategory"),
    path('blog/writer/<str:writer>',searchWriter,name="searchWriter")

]