from django.db import models
import datetime
# Create your models here.

class Appointment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=50)
    last_update = models.DateTimeField(auto_now=True)


    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50 , blank=True)
    price = models.IntegerField(default=0, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default=1)
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to = 'productshop/image', blank=True)
    
    @staticmethod
    def get_products_by_id_for_cartpage(ids):
        return Product.objects.filter(id__in=ids)
    
    
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.objects.all()
        
class Customer(models.Model):
    username = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False
    
    @staticmethod
    def get_customer_through_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False
        
class Order(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=60 , default='', blank = True)
    phone = models.CharField(max_length=60 , default='', blank = True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id ).order_by('-date')
        