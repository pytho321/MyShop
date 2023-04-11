from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from .models import *
from MyShop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
import random
from django.conf import settings
from django.core.mail import send_mail

def home(request):
    data = Product.objects.all()
    data =data[::-1]
    return render(request,"index.html",{"Data":data})


def shop(request,mc,sc,br):
    if(mc=="all" and sc=="all" and br=="all"):
        data = Product.objects.all()
    elif(mc!="all" and sc=="all" and br=="all"):
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc))
    elif(mc=="all" and sc!="all" and br=="all"):
        data = Product.objects.filter(subcat=SubCategory.objects.get(name=sc))
    elif(mc=="all" and sc=="all" and br!="all"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif(mc!="all" and sc!="all" and br=="all"):
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc),
                                     subcat=SubCategory.objects.get(name=sc))
    elif(mc!="all" and sc=="all" and br!="all"):
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc),
                                     brand=Brand.objects.get(name=br))
    elif(mc=="all" and sc!="all" and br!="all"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br),
                                     subcat=SubCategory.objects.get(name=sc))
    else:
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc),
                                     brand=Brand.objects.get(name=br),
                                     subcat=SubCategory.objects.get(name=sc))
    maincat = MainCategory.objects.all()
    subcat = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,"shop.html",{"Data":data,
                                        "Maincat":maincat,
                                        "Subcat":subcat,
                                        "Brand":brand,
                                        "MC":mc,
                                        "SC":sc,
                                        "BR":br,
                                        })

def product(request,id):
    product = Product.objects.get(id=id)
    if(request.method=='POST'):
        try:
            buyer = Buyer.objects.get(username = request.user)
        except:
            return HttpResponseRedirect('/profile/')
        cart = request.session.get('cart', None)
        q = (request.POST.get('q'))
        if(cart):
            if(str(id) in cart.keys()):
                cart[str(id)]+=int(q)
            else:
                cart.setdefault(str(id), int(q))
        else:
            cart = {str(product.id): q}
        request.session['cart'] = cart
        request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect('/cart/')
    return render(request,"product.html",{"Product":product})


@login_required(login_url='/login/')
def cartPage(request):
    try:
        buyer = Buyer.objects.get(username = request.user)
    except:
        return HttpResponseRedirect('/profile/')
    flushcart = request.session.get('flushcart', None)
    if(flushcart==True):
        request.session['cart']={}
        request.session['flushcart']=False
    cart = request.session.get('cart', None)
    products = []
    total = 0
    final = 0
    shipping = 0
    if (cart):
        for key,value in cart.items():
            p = Product.objects.get(id = int(key))
            products.append(p) 
            total= total + p.finalPrice * int(value)
        if(total<1000):
            shipping = 150
        else:
            shipping= 0
        final = total + shipping   
        if(request.method=='POST'):
            id = request.POST.get('id')
            q = int(request.POST.get('q'))
            cart[id]=q
            request.session['cart'] = cart
            request.session.set_expiry(60*60*24*30)
            return HttpResponseRedirect('/cart/')
    return render(request, 'cart.html', {'Products': products,
                                        "Total":total,
                                        'Final':final,
                                        "Shipping": shipping})


@login_required(login_url='/login/')
def deleteCart(request, id):
    cart = request.session.get('cart', None)
    if(cart):
        cart.pop(str(id))
        request.session['cart'] = cart
    return HttpResponseRedirect('/cart/')


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def checkout(request):
    try:
        buyer = Buyer.objects.get(username = request.user)
    except:
        return HttpResponseRedirect('/profile/')
    if(request.method=="POST"):
        cart = request.session.get('cart')
        if(cart is None):
            return HttpResponseRedirect('/cart/')
        else:
            check = CheckOut()
            check.buyer = buyer
            check.product = ""
            check.total = 0
            check.shipping = 0
            check.finalamount = 0
            for key,value in cart.items():
                check.product = check.product + key + ";" + str(value) + ','
                p = Product.objects.get(id = key)
                check.total = p.finalPrice * value
            if(check.total < 1000):
                check.shipping = 0
            check.finalamount = check.total+check.shipping
            check.save()
            mode = request.POST.get("mode")
            if (mode == "Cash on Delivery"):
                check.save()
                request.session['flushcart']= True
                return HttpResponseRedirect('/confirm/')
            else:
                orderAmount = check.finalamount*100
                orderCurrency = 'INR'
                paymentorder = client.order.create(dict(amount=orderAmount, currency = orderCurrency, payment_capture=1))
                paymentid = paymentorder['id']
                check.mode = 2
                check.save()
                return render(request, 'pay.html',{'amount': orderAmount,
                                                    'api_key': RAZORPAY_API_KEY,
                                                    'order_id': paymentid,
                                                    'User': buyer})
    else:
        cart = request.session.get('cart', None)
        product = []
        total = 0
        final = 0
        shipping = 0
        if (cart):
            for key,value in cart.items():
                p = Product.objects.get(id = int(key))
                product.append(p) 
                total= total + p.finalPrice * int(value)
            if(total<1000):
                shipping = 100
            else:
                shipping= 0
            final = total + shipping  
    return render(request, 'checkout.html',{'Product': product,
                                        "Total":total,
                                        'Final':final,
                                        "Shipping": shipping,
                                        "User": buyer})


@login_required(login_url='/login/')
def confirmationPage(request):
    return render(request, "confirm.html")


@login_required(login_url='/login/')
def payment(request):
    return render(request, 'pay.html')

def paymentSuccess(request, rpoid, rppid, rpsid):
    buyer = Buyer.objects.get(username = request.user)
    check = CheckOut.objects.filter(buyer = buyer)
    check = check[::-1]
    check = check[0]
    check.paymentid = rppid
    check.orderid = rpoid
    check.paymentsignature = rpsid
    check.paymentstatus = 2
    check.save()
    return HttpResponseRedirect("/confirm/")

def login(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/")
        else:
            messages.error(request,"Username or Password is Incorrect")
    return render(request,"login.html")

def signup(request):
    if(request.method=="POST"):
        actype = request.POST.get("actype")
        if(actype=="seller"):
            s = Seller()
            s.name = request.POST.get("name")
            s.username = request.POST.get("username")
            s.email = request.POST.get("email")
            s.phone = request.POST.get("phone")
            pward = request.POST.get('password')
            try:
                user = User.objects.create_user(username=s.username,password=pward)
                user.save()
                s.save()
                return HttpResponseRedirect('/login/')
            except:
                messages.error(request,"UserName already Taken!!!!")
        else:
            b = Buyer()
            b.name = request.POST.get("name")
            b.username = request.POST.get("username")
            b.email = request.POST.get("email")
            b.phone = request.POST.get("phone")
            pward = request.POST.get('password')
            try:
                user = User.objects.create_user(username=b.username,password=pward)
                user.save()
                b.save()
                return HttpResponseRedirect('/login/')
            except:
                messages.error(request,"UserName already Taken!!!!")
    return render(request,"signup.html")


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username = request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try: 
            seller = Seller.objects.get(username = request.user)
            return HttpResponseRedirect('/sellerprofile/', {'User': seller})
        except:
            buyer = Buyer.objects.get(username = request.user)
            return HttpResponseRedirect('/buyerprofile/')



@login_required(login_url='/login/')
def sellerprofile(request):
    seller = Seller.objects.get(username = request.user)
    products = Product.objects.filter(seller=seller)
    return render(request, 'sellerprofile.html', {'User': seller, 'Products': products})



@login_required(login_url='/login/')
def buyerprofile(request):
    buyer = Buyer.objects.get(username = request.user)
    wishlist = Wishlist.objects.filter(buyer = buyer)
    checkout = CheckOut.objects.filter(buyer = buyer)
    return render(request, 'buyerprofile.html', {'User': buyer, 'Wishlist': wishlist,'Checkout': checkout})


@login_required(login_url='/login/')
def updateprofile(request):
    user = User.objects.get(username = request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    try: 
        user = Seller.objects.get(username = request.user)
    except:
        user = Buyer.objects.get(username = request.user)
    if (request.method=='POST'):
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.addressline1 = request.POST.get('addressline1')
        user.addressline2 = request.POST.get('addressline2')
        user.addressline3 = request.POST.get('addressline3')
        user.pin = request.POST.get('pin')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        if(request.FILES.get('pic')):
            user.pic = request.POST.get('pic')
        user.save()
        return HttpResponseRedirect('/profile/')
    return render(request, 'updateprofile.html', {'User': user})


@login_required(login_url='/login/')
def addproduct(request):
    user = User.objects.get(username = request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    try: 
        user = Seller.objects.get(username = request.user)
    except:
        user = Buyer.objects.get(username = request.user)
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    seller = Seller.objects.get(username = request.user)
    if(request.method=='POST'):
        p = Product()
        p.name = request.POST.get('name')
        p.maincat = MainCategory.objects.get(name = request.POST.get('maincategory'))
        p.subcat = SubCategory.objects.get(name = request.POST.get('subcategory'))
        p.brand = Brand.objects.get(name = request.POST.get('brand'))
        p.basePrice = int(request.POST.get('basePrice'))
        p.discount = int(request.POST.get('discount'))
        p.finalPrice = p.basePrice - p.basePrice*p.discount//100
        p.size = request.POST.get('color')
        p.color = request.POST.get('color')
        p.stock = request.POST.get('stock')
        p.description = request.POST.get('description')
        p.seller = seller
        if(request.FILES.get('pic1')):
            p.pic1 = request.POST.get('pic1')
        if(request.FILES.get('pic2')):
            p.pic2 = request.POST.get('pic2')
        if(request.FILES.get('pic3')):
            p.pic3 = request.POST.get('pic3')
        if(request.FILES.get('pic4')):
            p.pic4 = request.POST.get('pic4')
        p.save()
        return HttpResponseRedirect('/sellerprofile/')
    return render(request, 'addproduct.html', {'MainCat': mainCat,
                                                'SubCat': subCat,
                                                'Brand': brand})

@login_required(login_url='/login/')
def editproduct(request, num):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    seller = Seller.objects.get(username=request.user)
    product = Product.objects.get(id = num)
    if(request.method=='POST'):
        product.name = request.POST.get('name')
        product.maincat = MainCategory.objects.get(name = request.POST.get('maincategory'))
        product.subcat = SubCategory.objects.get(name = request.POST.get('subcategory'))
        product.brand = Brand.objects.get(name = request.POST.get('brand'))
        product.basePrice = int(request.POST.get('basePrice'))
        product.discount = int(request.POST.get('discount'))
        product.finalPrice = product.basePrice - product.basePrice*product.discount//100
        product.size = request.POST.get('color')
        product.color = request.POST.get('color')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.seller = seller
        if(request.FILES.get('pic1')):
            product.pic1 = request.POST.get('pic1')
        if(request.FILES.get('pic2')):
            product.pic2 = request.POST.get('pic2')
        if(request.FILES.get('pic3')):
            product.pic3 = request.POST.get('pic3')
        if(request.FILES.get('pic4')):
            product.pic4 = request.POST.get('pic4')
        product.save()
        return HttpResponseRedirect('/sellerprofile/')
    return render(request, 'editproduct.html', {'MainCat': mainCat,
                                                'SubCat': subCat,
                                                'Brand': brand,
                                                'Product': product})



@login_required(login_url='/login/')
def deleteproduct(request, num):
    product = Product.objects.get(id = num)
    seller = Seller.objects.get(username=request.user)
    if(product.seller==seller):
        product.delete()
        return HttpResponseRedirect("/sellerprofile/")

    
@login_required(login_url='/login/')
def wishlistPage(request,num):
    product = Product.objects.get(id=num)
    buyer = Buyer.objects.get(username = request.user)    
    wishlist = Wishlist.objects.filter(buyer = buyer)
    flag = False
    for i in wishlist:
        if (i.product==product):
            flag = True
    if(flag==False):
        w = Wishlist()
        w.buyer=buyer
        w.product=product
        w.save()
    return HttpResponseRedirect("/buyerprofile/")


@login_required(login_url='/login/')
def deleteWishlist(request, num):
    buyer = Buyer.objects.get(username = request.user)  
    wishlist = Wishlist.objects.get(id = num)
    if(wishlist.buyer==buyer):
        wishlist.delete()
    return HttpResponseRedirect('/buyerprofile/')


def subscribePage(request):
    if(request.method=='POST'):
        email = request.POST.get('email')
        try:
            s = Subscribe.objects.get(email=email)
        except:
            subs = Subscribe()
            subs.email = email
            subs.save()

    return HttpResponseRedirect('/')


def contactUs(request):
    if(request.method=='POST'):
        c = ContactUs()
        c.name = request.POST.get('name')
        c.email = request.POST.get('email')
        c.phone = request.POST.get('phone')
        c.subject = request.POST.get('subject')
        c.messages = request.POST.get('messages')
        c.save()
        messages.success(request, 'Message Sent Successfully!!')
    return render(request, 'contact.html')

def forgotpassword(request):
    if(request.method=='POST'):
        username = request.POST.get('username')
        try: 
            user = Seller.objects.get(username=username)
        except:
            try: 
                user = Buyer.objects.get(username=username)
            except:
                messages.error(request, 'Username not found!')
                return HttpResponseRedirect('/forgotpassword/')
        user.otp= random.randint(1000,9999)
        user.save()
        subject = 'Welcome to Fashion World| OTP Generation'
        message = """
                    Hello!!
                    This is the otp generated email from My Shop
                    team.
                    Otp for setting your password is: %d    
                """%user.otp
        email_from = 'learnerpytho@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list)
        messages.success(request, 'OTP sent successfully')
        return HttpResponseRedirect('/confirmOTP/'+ username+'/')
    return render(request, 'forgotpassword.html')

def confirmOTP(request, username):
    if(request.method=='POST'):
        otp = int(request.POST.get('OTP'))
        try: 
            user = Seller.objects.get(username=username)
        except:
            user = Buyer.objects.get(username=username)
        if(user.otp==otp):
            return HttpResponseRedirect('/resetPassword/' + username +'/')
        else:
            messages.error(request, 'OTP invalid!!!')
    return render(request, 'confirmOTP.html')


def resetPassword(request, username):
    if(request.method=='POST'):
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        try: 
            user = Seller.objects.get(username=username)
        except:
            user = Buyer.objects.get(username=username)
        if(password==cpassword):
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request, 'Password and Confirm Password does not match!!!')
    return render(request, 'resetPassword.html')


def checkoutDelete(request, num):
    check = CheckOut.objects.get(id=num)
    buyer = Buyer.objects.get(username=request.user)
    if(check.buyer==buyer):
        check.delete()
    return HttpResponseRedirect('/buyerprofile/')

def payNow(request, num):
    try:
        buyer = Buyer.objects.get(username = request.user)
    except:
        return HttpResponseRedirect('/profile/')
    if(request.method=="POST"):
        check = CheckOut.object.get(id=num)
        orderAmount = check.finalamount*100
        orderCurrency = 'INR'
        paymentorder = client.order.create(dict(amount=orderAmount, currency = orderCurrency, payment_capture=1))
        paymentid = paymentorder['id']
        check.mode = 2
        check.save()
        return render(request, 'pay.html',{'amount': orderAmount,
                                            'api_key': RAZORPAY_API_KEY,
                                            'order_id': paymentid,
                                            'User': buyer})
    else:
        cart = request.session.get('cart', None)
        product = []
        total = 0
        final = 0
        shipping = 0
        if (cart):
            for key,value in cart.items():
                p = Product.objects.get(id = int(key))
                product.append(p) 
                total= total + p.finalPrice * int(value)
            if(total<1000):
                shipping = 100
            else:
                shipping= 0
            final = total + shipping  
    return render(request, 'checkout.html',{'Product': product,
                                        "Total":total,
                                        'Final':final,
                                        "Shipping": shipping,
                                        "User": buyer})


