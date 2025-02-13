from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from shop.models import Category, Product
from shop.forms import Userform


class Home(ListView):
    model=Category
    template_name='category.html'
    context_object_name='category'

class Products(DetailView):
    model=Category
    template_name="products.html"
    context_object_name='product'

class ProductDetails(DetailView):
    model=Product
    template_name='productdetails.html'
    context_object_name='item'

class Register(CreateView):
    model=User
    form_class=Userform
    template_name='register.html'
    success_url = reverse_lazy('shop:login')

    def form_valid(self,form):
        u=form.cleaned_data['username']
        p=form.cleaned_data['password']
        cp=form.cleaned_data['confirm_password']
        e=form.cleaned_data['email']
        f=form.cleaned_data['first_name']
        l=form.cleaned_data['last_name']
        if(cp!=p):
            form.add_error('confirm_password', 'Passwords do not match!')
            return self.form_invalid(form)
        u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
        u.save()
        return redirect('shop:login')


class Login(LoginView):
    template_name='login.html'


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:category')

class Addcategory(CreateView):
    model=Category
    fields=['name','desc','image']
    template_name='addcategory.html'
    success_url = reverse_lazy('shop:category')

class Addproduct(CreateView):
    model=Product
    fields=['name','desc','image','price','stock','category']
    template_name='addproduct.html'
    success_url = reverse_lazy('shop:category')

class Addstock(UpdateView):
    model=Product
    fields=['stock']
    template_name='addstock.html'
    #success_url = reverse_lazy('shop:category')
    def get_success_url(self):
         return reverse_lazy('shop:product_details',kwargs={'pk':self.object.id})
