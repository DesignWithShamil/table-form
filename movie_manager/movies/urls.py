from django.urls import path
from . import views

urlpatterns = [
     path('', views.create, name='create'),
    path('create/', views.create, name='create'),
    path('list', views.list, name='list'),
    path('add', views.add, name='add'),
    path('edit/<pk>', views.edit, name='edit'),
    path('delete/<pk>', views.delete, name='delete'),
   path('import/', views.impor, name='import'),
]
