from django.urls import path
from .views import index

urlpatterns =[
    path('',index,name="index"),#el index amarillo es para llamar el metodo creado en el views
    
   
]