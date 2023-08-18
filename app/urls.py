from django.urls import path
from app import views

urlpatterns = [
path('', views.home, name='home'),
path('membership/', views.membership, name='membership'),
path('productSale/', views.productSale, name='productSale'),
path('about/', views.about, name='about'),
path('contact/', views.contact, name='contact'),
path('appointment/', views.appointment, name='appointment'),
path('service/', views.service, name='service'),
path('signuppage/', views.signuppage , name='signuppage'),
path('loginpage/', views.loginpage , name='loginpage'),
path('logoutpage/', views.logoutpage , name='logoutpage'),
path('cart/' , views.cart , name='cart'),
path('checkout/' , views.checkout , name='checkout'),
path('order/' , views.order , name='order'),
]
