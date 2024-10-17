from django.db import models
from django.contrib.auth.models import User

STATE_CHOICE = (
    ("Punjab","Punjab"),
    ("Sindh","Sindh"),
    ("Khyber Pakhtunkhwa","Khyber Pakhtunkhwa"),
    ("Balochistan","Balochistan"),
    ("Gilgit-Baltistan","Gilgit-Baltistan"),
    
)
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    location = models.CharField(max_length=50)
    state = models.CharField(choices = STATE_CHOICE,max_length=30,default="pending")

    def __str__(self):
        return str(self.name)

class Brand(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

CATEGORY = (
    ("M","Mobiles"),
    ("L","Laptops"),
)


class Product(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE )
    category = models.CharField(choices=CATEGORY,max_length=100)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media')
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    storage = models.CharField(max_length=50,default='Unknown')
    trending = models.BooleanField(default=False)


    def __str__(self):
        return (self.title)
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    add_at = models.DateField(auto_now_add=True, null=True, blank=True)



class Shipping(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    company_name = models.CharField(max_length=200,null=True)
    area_code = models.IntegerField(null=True)
    primary_phone = models.IntegerField(null=True)
    street_address = models.CharField(max_length=2000,null=True)
    zip_code = models.IntegerField(null=True)
    buisness_address = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name



    
class Payment(models.Model):
    holder_name = models.CharField(max_length=200),
    card_number = models.IntegerField(null = True)
    expiry_month = models.CharField(max_length=20)
    expiry_year = models.CharField(max_length=20)
    CSC = models.IntegerField(null = True)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)
    review = models.CharField(max_length=500)

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    discounted_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=100)