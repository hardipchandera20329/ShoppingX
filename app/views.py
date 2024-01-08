from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,Orderplaced
from .forms import CustomerRegiForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required #function base
from django.utils.decorators import method_decorator # class base


# def home(request):
#  return render(request, 'app/home.html')
# class Base View:::::1
class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(categary='TW')
        bottomwears=Product.objects.filter(categary='BW')
        mobiles=Product.objects.filter(categary='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})     
     
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
# class base view:::2
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0   
        product=Product.objects.get(pk=pk)
        already_incart=False
        if request.user.is_authenticated:    #without login detrail show<<<<<<
            totalitem=len(Cart.objects.filter(user=request.user))
            already_incart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'already_incart':already_incart,'totalitem':totalitem})
        # totalitem=0 
        # totalitem=len(Cart.objects.filter(user=request.user))
# 3
def mobile(request,data=None):
    if data == None:
        mobiles=Product.objects.filter(categary="M")
    elif data == "Vivo" or data == "Samsung":
        mobiles=Product.objects.filter(categary="M").filter(brand=data)
    elif data == "below":
        mobiles=Product.objects.filter(categary="M").filter(discounted_price__lt=10000)
        # lt-->lessthan
        # gt-->greterthan
    elif data == "above":
        mobiles=Product.objects.filter(categary="M").filter(discounted_price__gt=10000)        
    return render(request, 'app/mobile.html',{'mobiles':mobiles})    

# 4
class CustomerRegiView(View):
    def get(self,request):
        form=CustomerRegiForm()
        return render(request,'app/customerregistration.html',{'form':form})    
    def post(self,request):
        form=CustomerRegiForm(request.POST)
        if form.is_valid():
           messages.success(request,"Congratulations !! Registered Successfully")
           form.save()
        return render(request,'app/customerregistration.html',{'form':form})   

#5 ===> urls ==>LoginForm
# def login(request):
#  return render(request, 'app/login.html')

# 6==>urls 
# def logout():

# 7===> urls ==>MyPasswordChangeForm
# def change_password(request):
#  return render(request, 'app/changepassword.html')

# 8
# def profile(request):
#  return render(request, 'app/profile.html')
@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
           usr=request.user
           name=form.cleaned_data['name']
           locality=form.cleaned_data['locality']
           city=form.cleaned_data['city']
           state=form.cleaned_data['state']
           zipcode=form.cleaned_data['zipcode']
           reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
           reg.save()
           messages.success(request,"Congratulations !! Profile Updated Successfully")
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

# 9
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

# 10
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

# 11
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount=amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request, 'app/empty.html')

# 12
def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & (Q(user=request.user)))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)
    
# 13
def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & (Q(user=request.user)))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)    

# 14
def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & (Q(user=request.user)))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)
    
#15 
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    # print('========>',add)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

# 16
@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

# 17
def orders(request):
    op=Orderplaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def buy_now(request):
 return render(request, 'app/buynow.html')
