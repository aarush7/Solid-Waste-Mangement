"""swm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from invt import views
from django.shortcuts import render
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('register/', views.register,name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('home/', views.home,name='home'),
    path('home/waste-form', views.waste_form,name='waste_form'),
    path('home/tv-form', views.tv_form,name='tv_form'),
    path('home/pp-form', views.pp_form,name='pp_form'),
    path('home/lf-form', views.lf_form,name='lf_form'),

    path('home/tv/edit_item/<uuid:pk>', views.update_tv, name="update_tv"),
    path('home/pp/edit_item/<uuid:pk>', views.update_pp, name="update_pp"),
    path('home/lf/edit_item/<uuid:pk>', views.update_lf, name="update_lf"),

    path('home/tv/delete/<uuid:pk>', views.delete_tv, name="delete_tv"),
    path('home/lf/delete/<uuid:pk>', views.delete_lf, name="delete_lf"),
    path('home/pp/delete/<uuid:pk>', views.delete_pp, name="delete_pp"),
    path('home/wasteml/export', views.export, name="export"),
    path('home/wasteml/graph', views.graphh, name="graph"),
    path('home/wasteml/list',views.WasteMLView.as_view(),name="wasteml_data"),
]
