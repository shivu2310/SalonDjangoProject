from django.shortcuts import render,redirect , HttpResponseRedirect
from .models import Appointment,Product,Category,Customer,Order
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password , check_password

from app.middlewares.auth import auth_middleware



# Create your views here.

def home (request):
    return render (request, 'home.html')

def membership (request):
    return render (request, 'membership.html')

def productSale (request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.objects.all()
        procount=Product.objects.all().count()
   
    
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.objects.all()
        
        data = {}
        data['product'] = products
        data['categories'] = categories
        data['procount'] = procount
    
        return render (request, 'productSale.html' , data)
    else:
        product_id = request.POST.get('productcart')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity-1
                else:
                    cart[product_id] = quantity+1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart']=cart
    
        return redirect('/productSale')
        
        
        
        
        
        
        
        
def about (request):
    return render (request, 'about.html')

def contact (request):
    return render (request, 'contact.html')

def appointment (request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('phone')
        errory = None
        if (not email):
            errory = "Please Enter Email Field"
        elif ( '@' not in email ):
            errory = " @ is Missing "
        elif (not contact):
            errory = "Please Enter Phone Number Field"
        elif (not name):
            errory = "Please Enter Address Field"
        elif (len(contact)>10):
            errory = "Exceed the Limit of Phone Number Digit"
            
        if not errory:
            appointment = Appointment(name=name , email=email , contact=contact)
            appointment.save()
            messages.info(request, ' Your Appointment has booked')
            send_mail(
                'Appointment has Booked in Moni-Ra Salon ',
                'Congratulation ! Your Appointment in Moni-Ra Salon has been Booked. Moni-Ra Team will contact you on Your Contact Number which You mentioned while Booking Appointment and Allocate Time Schedule.ThankYou For Booking In Moni-Ra Salon.',
                'monirasalonbooking@gmail.com',
                [email],
                fail_silently=False,
            )            
            send_mail(
                'Booking has come  ',
                ' An Appointment has been Booked by User/Customer. Please Check and contact him/her on Contact Number and Allocate Time Schedule.',
                'monirasalonbooking@gmail.com',
                ['monirasalonbooking@gmail.com'],
                fail_silently=False,
            )            
            
            

            
            
        else:
            error = {'error': errory}
            return render (request, 'appointment.html', error)
    return render (request, 'appointment.html')

def service (request):
    return render (request, 'service.html')


def signuppage(request):
    if request.method == 'GET':
        return render (request, 'signuppage.html')
    else:
        post=request.POST.get
        email = post('email')
        phone = post('phone')
        password = post('password')
        again_password = post('password_again')
        username = post('username')
        #value
        value = {
            'email' : email,
            'phone' : phone,
            'username' : username,
            
        }

        #validation
        error = None
        customer = Customer(username = username , phone = phone , email = email , password = password )    
        if not email:
            error = "Email Field is Required"
        elif not username:
            error = "Username is Required"
        elif len(username) < 4 :
            error = "Username must be 4 Character Long"
        elif not phone:
            error = "Phone Number Field is Required"
        elif len(phone) < 10:
            error = "Phone Number must be 10 Digits"
        elif not password:
            error = "Password must be Required"
        elif not again_password:
            error = "Please Re-Enter The Password"
        elif len(password) < 8:
            error = "Password must be 8 Character/Number Long"
        elif (password != again_password):
            error = "Password and Confirm Password is not Matching"
        elif customer.isExists():
            error = "This Email Address has been Already Registered in our Database"
        if not error:    
            customer.password = make_password(customer.password)
            customer.save()
            messages.success(request, ' Congratulation! Your Account Has Been Created ')
            return redirect('/productSale')
        else:
            data = {
                'error': error , 'filler': value 
            }
            return render (request, 'signuppage.html', data)




def loginpage (request):
    if request.method == 'GET':
        loginpage.return_url = None
        loginpage.return_url = request.GET.get('return_url')
        return render (request, 'loginpage.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        customer =    Customer.get_customer_through_email(email) 

        error = None

        if customer :
            flag = check_password(password , customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                if loginpage.return_url:
                    return HttpResponseRedirect(loginpage.return_url)
                else:
                    loginpage.return_url = None
                    return redirect('/productSale')
            else:
                error = 'Email or Password is invalid'
        
        else:
            error = 'Email or Password is invalid'
        return render (request, 'loginpage.html', {'error' : error })
        

def logoutpage(request):
    request.session.clear()
    return redirect ('/loginpage')

def cart(request):
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id_for_cartpage(ids) 
            
        return render(request, 'cartpage.html' , {'products' : products})

        
    
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        print(customer)
        cart = request.session.get('cart')   # in this cart we have quantity and in products has products 
        products = Product.get_products_by_id_for_cartpage(list(cart.keys()))   #cart.keys()= Has all Product ids 

        print(address , phone, customer , cart , products )
      
        for product in products:
            order = Order(customer = Customer( id = customer) , product = product , price = product.price , address = address , phone = phone  )
            if customer:
                order.save()
            else:
                return redirect('loginpage')
        request.session['cart'] = {}

        return redirect ('/cart')


@auth_middleware
def order(request):
    
    
    customer = request.session.get('customer_id')
    orders = Order.get_orders_by_customer(customer)
    return render(request, 'order.html' , {'orders' : orders })