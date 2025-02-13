import razorpay
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart, Payment, Order_details


@login_required
def addtocart(request,i):
    u=request.user
    p=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=u,product=p)
        if(p.stock > 0):
            c.quantity += 1
            c.save()
            p.stock -= 1
            p.save()
    except:
        c=Cart.objects.create(user=u,product=p,quantity=1)
        if(p.stock > 0):
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cartview')

@login_required
def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'total':total}
    return render(request,'cart.html',context)

@login_required
def cart_decrement(request,i):
    u=request.user
    p=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity > 1):
            c.quantity -= 1
            c.save()
            p.stock += 1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

@login_required
def cart_delete(request,i):
    u=request.user
    p=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=u,product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')

def orderform(request):
    if(request.method=='POST'):
        a=request.POST['a']
        ph=request.POST['p']
        pin=request.POST['pin']
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total)

        #Razorpay client connection
        client=razorpay.Client(auth=('rzp_test_4kwmjAspSRBmzG','ok4MsbrJu8qw6Vk4WTvjtXU6'))
        #Razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']
        status=response_payment['status']

        if (status=="created"):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,phone=ph,address=a,pin=pin,order_id=order_id,no_of_items=i.quantity)
                o.save()
            context={'payment':response_payment,'name':u.username}
            return render(request,'payment.html',context)

    return render(request,'orderform.html')
@csrf_exempt
def payment_status(request,p):
    user=User.objects.get(username=p) #retrive user object
    login(request,user)
    response=request.POST #razorpay responds after successful payment
    print(response)

    # to check the validity of razorpay payment details received by application
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }
    client=razorpay.Client(auth=('rzp_test_4kwmjAspSRBmzG','ok4MsbrJu8qw6Vk4WTvjtXU6'))
    try:
        status=client.utility.verify_payment_signature(param_dict)     #for checking the payment details we pass param_dict to verify_payment_signature function
        print(status)
    except:
        pass

    p=Payment.objects.get(order_id=response['razorpay_order_id'])
    p.paid=True
    p.razorpay_payment_id=response['razorpay_payment_id']
    p.save()

    o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
    for i in o:
        i.payment_status="completed"
        i.save()

    c=Cart.objects.filter(user=user)
    c.delete()
    return render(request,'payment_status.html')

def orderview(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status='completed')
    context={'orders':o}
    return render(request,'order.html',context)

