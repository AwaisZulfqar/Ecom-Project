from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Shipping,Payment,Contact,Review
from django import forms 
class SignupForm(UserCreationForm):
    usable_password = None
   
    password2 = forms.CharField(widget=forms.PasswordInput,label = 'Confirm Password')
    class Meta:
        model = User
        fields = ['username','email']
        labels = {
            'email': 'Email'
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name','title','review')
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write your review here...'}),
        }




