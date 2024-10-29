from django.shortcuts import render,redirect
from .forms import SignupForm,ShippingForm,PaymentForm,ContactForm,ReviewForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.views import View
from .models import Product,Brand,Cart,Contact,Review,OrderProduct
from django.db.models import Q
import stripe
import datetime
from webproject import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Product
# Create your views here.


# Registeration___________________________________________
def sign_up(request):
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Account created Succefully')
            return HttpResponseRedirect('/login/')
        
    
    else:
        fm = SignupForm()
    return render (request, 'signup.html',{'form':fm})


# def Home(request):
#     return render(request,'index.html')
#jdfajsdkfads
class HomeView(View):
        def get(self,request):
            mobiles = Product.objects.filter(category = "M")
            laptops = Product.objects.filter(category = "L")
            trending =  Product.objects.filter(trending=True)
            brands =  Brand.objects.all()
             
            return render(request,'index.html',{'mobiles':mobiles,'laptops':laptops,'trending':trending,'brands':brands})
        

#Login M view________________________________________________
def userlogin(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data = request.POST )
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate (username = uname, password = upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')

    else:
        fm = AuthenticationForm()
    return render(request,'login.html',{'form':fm})


#Logout View______________________________________________
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')



def about_us(request):
    return render(request,'about_us.html')

def checkout_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    if product_id:
        product = Product.objects.get(id = product_id)
        Cart(user = user , product=product).save()
    carts=Cart.objects.filter(user=user)
    amount=0.0
    shipping=150
    total_amount=0.0
    cart_product = Cart.objects.filter(user=user)
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            total_amount=amount+shipping
        return render(request,'checkout_cart.html',{'carts':carts,'amount':amount,'total_amount':total_amount})
# def  checkout_cart(request):
#     return render(request,'checkout_cart.html')
# class checkout_cart(View):
#     def get(self,request):
#         if request.user.is_authenticated:
#             user = request.user
#             product_id = request.GET.get('prod_id')
#             if product_id:
#                 product = Product.objects.get(id = product_id)
#                 Cart(user = user , product=product).save()

#             carts = Cart.objects.filter(user=user)

#             amount = 0
#             shipping = 0
#             total_amount = 0

#             for item in carts:
#                 total_price = item.product.price * item.quantity 
#                 shipping += item.quantity * 8
#                 amount += total_price  
#                 total_amount = amount + shipping
#             return render(request,'checkout_cart.html',{"carts":carts})
#         else:
#             return redirect('login')
def delete_data(request,id):
    item = Cart.objects.get(pk=id,user=request.user)
    item.delete()
    return HttpResponseRedirect('/checkout_cart/')
    
def increase(request,id):
    item = Cart.objects.get(id=id ,user=request.user)
    item.quantity +=1
    item.save()
    return redirect('/checkout_cart/')
    
def decrease(request,id):
    item = Cart.objects.get(id=id, user=request.user)
    if item.quantity >1:
        item.quantity -=1 
        item.save()
    return redirect('/checkout_cart/')
        

    
    
# class showcart(View):
#     def get(self,request):
#         if request.user.is_authenticated:
#             user = request.user
            



# def  checkout_complete(request):
#     return render(request,'checkout_complete.html')
def checkout_complete(request):
    items = Cart.objects.filter(user=request.user).first()
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        discounted_price=item.product.discounted_price
        image=item.product.image
        title = item.product.title
        quantity = item.quantity
        odr_prd_mod = OrderProduct.objects.create(user=request.user,title=title,image=image,discounted_price=discounted_price,quantity=quantity)
        odr_prd_mod.save()

    date = datetime.datetime.now()
    delivery_date_delta = datetime.timedelta(days=2)
    delivery_date = date + delivery_date_delta
    
    transaction = "REF" 
    bank_authorised_code = "AUTH" 
    cart_items_list = list(cart_items)
    cart_items.delete()
    context = {
        'items': items,
        'cart_items': cart_items_list, 
        'date': date,
        'delivery_date': delivery_date,
        'transaction_reference_no': transaction,
        'bank_authorised_code': bank_authorised_code,
    }
    return render(request, "checkout_complete.html", context)


# def  checkout_info(request):
#     return render(request,'checkout_info.html')
class checkout_info(View):
    def get(self,request):
        if request.user.is_authenticated:
            fm = ShippingForm()
            return render(request,'checkout_info.html',{'form':fm})
        else:
            return redirect('/login/')

    def post(self,request):
        if request.user.is_authenticated:
            fm = ShippingForm(request.POST)
            if fm.is_valid():
                fm.save()
                fm = ShippingForm()
            return render(request,'checkout_info.html',{'form':fm})
        else:
            return redirect('/login/')

def checkout_payment(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    if user_cart_items.exists():
        line_items = []
        for cart_item in user_cart_items:
            product = cart_item.product
            name = product.title
            price = product.discounted_price
            line_items.append({
                'price_data': {
                    'currency': 'pkr',
                    'unit_amount': max(1, int(price * 100)),
                    'product_data': {'name': name},
                },
                'quantity': cart_item.quantity,
            })
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout_complete')),
            cancel_url=request.build_absolute_uri(reverse('Home')),
            line_items=line_items,
            )
                # return HttpResponse('Success')
        return redirect(session.url)
    return render(request, "checkout_payment.html")

class ContactView(View):
    model = Contact
    template_name = 'contact_us.html'

    def get(self,request):
        fm = ContactForm()
        return render(request,self.template_name,{"form":fm})


    def post(self,request):
        fm = ContactForm(request.POST)
        if fm.is_valid:
            fm.save()
            return redirect('/')

        return render(request,self.template_name,{"form":fm})



def  faq(request):
    return render(request,'faq.html')


def  index_fixed_header(request):
    return render(request,'index_fixed_header.html')


def  index_inverse_header(request):
    return render(request,'index_inverse_header.html')


def my_account(request):
    return render(request,'my_account.html')

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        reviews = Review.objects.filter(product = product)
        fm = ReviewForm()
        return render(request,'product_detail.html',{"product":product,'form':fm,'reviews':reviews})
    def post(self,request,pk):
        product = Product.objects.get(pk=pk)
        fm = ReviewForm(request.POST)
        if fm.is_valid():
            review = fm.save()
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=pk)
        reviews = Review.objects.filter(product = product)
        
        return render(request,'product_detail.html',{"product":product,'form':fm,'reviews':reviews})
        

def product(request):
    return render(request,'product.html')


def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = Product.objects.filter(Q(title__icontains = searched)|Q(brand__name__icontains=searched))
        return render(request,'search_results.html',{'searched':searched,'results':results,})

