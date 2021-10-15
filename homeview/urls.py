from django.contrib import admin  
from django.urls import path  
from homeview import views  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),
    path('',views.login),  
    path('signin', views.signin),
    path('signout', views.signout),
    path('main', views.main),
    path('file_upload', views.file_upload),
    path('log_history', views.log_history),
    path('create_user', views.create_user),
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),
    path('detector', views.detector),
    path('trainmodel', views.trainmodel),
    path('clearmodel', views.clearmodel),
    path('getmessage1', views.getmessage1),
    path('getmessage2', views.getmessage2),
]  