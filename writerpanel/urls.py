from django.urls import path
from .views import panel,displayFrom,insertData,deleteData,editData,updateData
urlpatterns = [
    path('', panel,name="panel"),
    path('displayFrom',displayFrom,name='displayFrom'),
    path('insertData',insertData,name='insertData'),
    path('deleteData/<int:id>',deleteData,name='deleteData'),
    path('editData/<int:id>',editData,name='editData'),
    path('updateData/<int:id>',updateData,name='updateData')
]