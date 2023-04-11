from distutils.command.upload import upload
from django.db import models

class MainCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,blank=True,null=True)
    addressline2 = models.CharField(max_length=100,default=None,blank=True,null=True)
    addressline3 = models.CharField(max_length=100,default=None,blank=True,null=True)
    pin = models.CharField(max_length=10,default=None,blank=True,null=True)
    city = models.CharField(max_length=20,default=None,blank=True,null=True)
    state = models.CharField(max_length=20,default=None,blank=True,null=True)
    pic = models.ImageField(upload_to="images/", default='None', blank=True, null=True)
    otp = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)+" "+self.username




class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    maincat = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subcat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    basePrice = models.IntegerField()
    discount = models.IntegerField(default=0)
    finalPrice = models.IntegerField()
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    description = models.TextField()
    stock = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
    pic1 = models.ImageField(upload_to="images/", default='None', blank=True, null=True)
    pic2 = models.ImageField(upload_to="images/", default='None', blank=True, null=True)
    pic3 = models.ImageField(upload_to="images/", default='None', blank=True, null=True)
    pic4 = models.ImageField(upload_to="images/", default='None', blank=True, null=True)

    def __str__(self):
        return str(self.id)+" "+self.name+" "


class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,blank=True,null=True)
    addressline2 = models.CharField(max_length=100,default=None,blank=True,null=True)
    addressline3 = models.CharField(max_length=100,default=None,blank=True,null=True)
    pin = models.CharField(max_length=10,default=None,blank=True,null=True)
    city = models.CharField(max_length=20,default=None,blank=True,null=True)
    state = models.CharField(max_length=20,default=None,blank=True,null=True)
    pic = models.ImageField(upload_to="images/", default='None', blank=True, null=True)
    otp = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)+" "+self.username

class Wishlist(models.Model):
    id =  models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+" "+self.buyer.username


choice = ((1,"Not Packed yet"), (2,"Items Packed"), (3,"Out for Delivery"), (4,"Delivered"))
payment = ((1,"Pending"), (2,"Done"))
mode = ((1,"Cash on Delivery"), (2,"Online Payment"))

class CheckOut(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.CharField(max_length=10)
    shipping = models.IntegerField()
    finalamount = models.IntegerField()
    total = models.IntegerField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(choices = choice, default = 1)
    paymentstatus = models.IntegerField(choices = payment, default=1)
    mode = models.IntegerField(choices = mode, default = 1)
    time = models.DateTimeField(auto_now=True)
    orderid  = models.CharField(max_length=50, blank=True, null=True,default=True)
    paymentid  = models.CharField(max_length=50, blank=True, null=True,default=True)
    paymentsignature  = models.CharField(max_length=50, blank=True, null=True,default=True)


    def __str__(self):
        return str(self.id)+" "+self.buyer.username + " "+ str(self.active)


class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)+" "+ self.email


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=20)
    messages = models.CharField(max_length=20)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)+ " " + self.name + ' ' +self.email