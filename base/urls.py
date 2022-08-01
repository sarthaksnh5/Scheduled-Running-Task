from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginUser, name='home'),
    path('delete/<int:id>', views.deleteEntry, name='delete'),
    path('base', views.index, name='base'),    
    path('add', views.addFiles, name='add'),
    path('file', views.changeSchedule, name='change'),
    path('getData', views.getFile, name='files'),
    path('logout', views.logoutUser, name='logout')
]
