from django.urls import path
from . import views
urlpatterns=[
    path('',views.register,name='register'),
    path('set-password/',views.set_password,name='set_password'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
]