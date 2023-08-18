from django.contrib import admin

# Register your models here.


from .models import Appointment,Product,Category,Customer,Order

class AdminAppointment(admin.ModelAdmin):
    list_display = ['name' , 'contact' , 'email' , 'last_update']

class AdminProduct(admin. ModelAdmin):
    list_display = ['name' , 'price' , 'category']
    
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['username', 'email' , 'phone' ]
    
class AdminOrder(admin.ModelAdmin):
    list_display = ['customer' ,'product' , 'phone']

admin.site.register(Appointment , AdminAppointment)
admin.site.register(Product , AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Customer , AdminCustomer)
admin.site.register(Order,AdminOrder)