from django.shortcuts import render, get_object_or_404
from .models import Product
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
# Create your views here.
def base(request):
    return render(request, 'ecom_app/base.html')

def home(request):
    return render(request, 'ecom_app/home.html')

def products(request):
    return render(request, 'ecom_app/products.html')

def electronic(request):
    return render(request, 'ecom_app/electronic.html')

def appliance(request):
    return render(request, 'ecom_app/appliance.html')

def gaming(request):
    return render(request, 'ecom_app/gaming.html')

def fashion(request):
    return render(request, 'ecom_app/fashion.html')

def accessories(request):
    return render(request, 'ecom_app/accessories.html')

def beauty(request):
    return render(request, 'ecom_app/beauty.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecom_app/description.html', {'product': product})

class RegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'ecom_app/registration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'ecom_app/registration.html', {'form':form})

# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request, 'description.html', {'product': product})

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'ecom_app/profile.html')