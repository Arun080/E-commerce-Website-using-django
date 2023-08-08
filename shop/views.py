from django.http import JsonResponse
from django.shortcuts import render,redirect
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def success(request):
    if request.user.is_authenticated:
        return render(request,"shop/success.html")
    else:
        return redirect("/")

def payment(request):
    if request.user.is_authenticated:
         return render(request,"shop/onlinepay.html")
    else:
        return redirect("/")
    
def favview_page(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")
    
def user_data(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pno=request.POST.get('pno')
        address=request.POST.get('address')
        Userdata.objects.create(fname=fname,lname=lname,email=email,pno=pno,address=address )
        return render(request,'shop/payment.html')
    return render(request, 'shop/form.html')

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
    
def remove_cart(request,cid):
    cart_item=Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect("/cart")

def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favview_page")

def fav_page(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id = product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already in Favourite '},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Producted Added to favourite'},status=200)
        else:
           return JsonResponse({'status':'Login to Add Favourite'},status=200) 
     else:
       return JsonResponse({'status':'Invalid Access'},status=200)

def add_to_cart(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id = product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already in Cart '},status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added to cart '},status=200)
                    else:
                        return JsonResponse({'status':'Stock Not Available'},status=200)
        else:
           return JsonResponse({'status':'Login to Add cart'},status=200) 
     else:
       return JsonResponse({'status':'Invalid Access'},status=200)
       


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out succesfully ")
    return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully...!")
                return redirect("/")
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect("/login")
    return render(request,"shop/login.html")



def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form =CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success..You can Login Now")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})


def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})


def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such category found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No such Products found")
            return redirect('collections')
    else:
        messages.error(request,"No such category found")
        return redirect('collections')