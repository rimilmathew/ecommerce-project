"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from shop import views

app_name="shop"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name='category'),
    path('products/<int:pk>',views.Products.as_view(),name='products'),
    path('product_details/<int:pk>',views.ProductDetails.as_view(),name='product_details'),
    path('register',views.Register.as_view(),name='register'),
    path('login',views.Login.as_view(), name='login'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('addcategory',views.Addcategory.as_view(),name='addcategory'),
    path('addproduct',views.Addproduct.as_view(),name='addproduct'),
    path('addstock/<int:pk>',views.Addstock.as_view(),name='addstock'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

