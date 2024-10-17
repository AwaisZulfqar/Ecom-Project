from django.urls import path
from Ecom import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.HomeView.as_view(),name = 'Home'),
    path('signup/',views.sign_up,name = 'signup'),
    path('login/',views.userlogin,name = 'login'),
    path('logout/',views.userlogout,name = 'logout'),
    path('about_us/',views.about_us ,name = 'about_us'),
    path('checkout_cart/',views.checkout_cart,name = 'checkout_cart'),
    path('delete/<int:id>/',views.delete_data,name = 'delete'),
    path('decrease/<int:id>/',views.decrease ,name = "decrease"),
    path('increase/<int:id>/',views.increase ,name = "increase"),
    path('checkout_complete/',views.checkout_complete ,name = 'checkout_complete'),
    path('checkout_info/',views.checkout_info.as_view() ,name = 'checkout_info'),
    path('checkout_payment/',views.checkout_payment,name = 'checkout_payment'),
    path('contact_us/',views.ContactView.as_view() ,name = 'contact_us'),
    path('faq/',views.faq ,name = 'faq'),
    path('index_fixed_header/',views.index_fixed_header ,name = 'index_fixed_header'),
    path('index_inverse_header/',views.index_inverse_header ,name = 'index_inverse_header'),
    path('my_account/',views.my_account ,name = 'my_account'),
    path('product_detail/<int:pk>',views.ProductDetail.as_view() ,name = 'product_detail'),
    path('product/<int:pk>',views.product ,name = 'product'),
    path('search/',views.search_result ,name = 'search'),
] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)