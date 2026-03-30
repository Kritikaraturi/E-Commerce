from django.shortcuts import render, get_object_or_404
from .models import Product, Customer
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='login')
def profile(request):

    profile = Customer.objects.filter(user=request.user).first()
    print("hello kjdfksjdkfj sdfjdskjfksdjfksdjfkjds")
    # POST request handle karo pehle
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)

        print("POST HIT ✅")

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()

            print("DATA SAVED ✅")

            return redirect("profile2")   # ✔ correct

        else:
            print("ERROR:", form.errors)

    else:
        form = CustomerProfileForm(instance=profile)

    return render(request,'ecom_app/profile.html', {'form': form,})

@login_required(login_url='login')
def get_curent_user_profile(request):
    profile = Customer.objects.filter(user=request.user).first()

    if not profile:
        return redirect("profile")

    return render(request, "ecom_app/profile2.html", {"profile": profile})

def changepassworddone(request):
    return render(request, 'ecom_app/changepassworddone.html')