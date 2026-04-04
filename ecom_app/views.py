from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import viewsets
from .models import Product, Customer, Cart, OrderPlaced
from .serializers import ProductSerializer, CustomerSerializer, CartSerializer, OrderPlacedSerializer, UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


# Create your views here.
def base(request):
    return render(request, 'ecom_app/base.html')

def home(request):
    return render(request, 'ecom_app/home.html')

def products(request):
    return render(request, 'ecom_app/products.html')

def electronic(request):
    products = Product.objects.filter(category='Electronics')
    return render(request, 'ecom_app/electronic.html', {'products': products})

def appliance(request):
    products = Product.objects.filter(category='Home Appliances')
    return render(request, 'ecom_app/appliance.html', {'products': products})

def gaming(request):
    products = Product.objects.filter(category='Gaming')
    return render(request, 'ecom_app/gaming.html', {'products': products})

def fashion(request):
    products = Product.objects.filter(category='Fashion')
    return render(request, 'ecom_app/fashion.html', {'products': products})

def accessories(request):
    products = Product.objects.filter(category='Accessories')
    return render(request, 'ecom_app/accessories.html', {'products': products})

def beauty(request):
    products = Product.objects.filter(category='Beauty')
    return render(request, 'ecom_app/beauty.html', {'products': products})

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

@login_required
def add_to_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')

        product = Product.objects.get(id=prod_id)
        user = request.user

        item = Cart.objects.filter(user=user, product=product).first()

        if item:
            item.quantity += int(quantity)
            item.save()
        else:
            Cart.objects.create(
                user=user,
                product=product,
                quantity=int(quantity)
            )

    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_amount = 0
    for item in cart_items:
        total_amount += item.product.discounted_price * item.quantity

    return render(request, 'ecom_app/add_to_cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

def remove_from_cart(request, id):
    item = Cart.objects.get(id=id, user=request.user)
    item.delete()
    return redirect('cart')

from .models import Cart, Customer

import razorpay
from django.conf import settings

@login_required
def checkout(request):
    user = request.user

    # user profile
    profile = Customer.objects.filter(user=user).first()

    buy_now_data = request.session.get('buy_now')

    total_amount = 0

    print(request.session.get('buy_now'))

    # 🔥 BUY NOW CASE
    if buy_now_data:
        product = Product.objects.get(id=buy_now_data['product_id'])
        quantity = buy_now_data['quantity']

        cart_items = [{
            'product': product,
            'quantity': quantity
        }]

        total_amount = product.discounted_price * quantity

    # 🔥 CART CASE
    else:
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            total_amount += item.product.discounted_price * item.quantity

    # 🔥 Razorpay order create
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))  

    payment = client.order.create({
        "amount": int(total_amount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, 'ecom_app/checkout.html', {
        'profile': profile,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

@login_required
def payment_success(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    buy_now_data = request.session.get('buy_now')

    if buy_now_data:
        product = Product.objects.get(id=buy_now_data['product_id'])
        quantity = buy_now_data['quantity']

        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=product,
            quantity=quantity
        )

        del request.session['buy_now']   
    else:
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,     # ✔ required
                product=item.product,  # ✔ object pass karna hai
                quantity=item.quantity
            )

        # 🧹 cart clear
        cart_items.delete()

    return render(request, "ecom_app/order_success.html")

@login_required
def my_orders(request):
    user = request.user

    orders = OrderPlaced.objects.filter(user=user).order_by('-ordered_date')

    return render(request, "ecom_app/orders.html", {
        "orders": orders
    })

@login_required
def buy_now(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Product.objects.get(id=prod_id)

        request.session['buy_now'] = {'product_id': product.id,'quantity': quantity}

        return redirect('checkout')
    
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['reset_user'] = user.id
            request.session.modified = True
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No user with this email.')
    return render(request, 'ecom_app/forgot_password.html')



def reset_password(request):
    user_id = request.session.get('reset_user')
    if not user_id:
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'ecom_app/reset_password.html')

# Product CRUD
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Customer CRUD
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Cart CRUD
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# Order CRUD
class OrderPlacedViewSet(viewsets.ModelViewSet):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer




class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class CustomerAdminViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

class OrderAdminViewSet(viewsets.ModelViewSet):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer
    permission_classes = [AllowAny]