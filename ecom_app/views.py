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
from django.core.paginator import Paginator
import random
from django.core.mail import send_mail

# Create your views here.
def base(request):
    return render(request, 'ecom_app/base.html')

# def home(request):
#     return render(request, 'ecom_app/home.html')

# def home(request):
#     featured_products = Product.objects.all()[:10]

#     return render(
#         request,
#         'ecom_app/home.html',
#         {
#             'featured_products': featured_products
#         }
#     )

def home(request):
    featured_products = Product.objects.all()[:10]
    
    # Har category ke liye 4 products fetch karein
    categories = ['Electronics', 'Home Appliances', 'Fashion']
    
    category_products = {}
    for category in categories:
        category_products[category] = Product.objects.filter(category=category)[:7]  # 7 products per category
    
    return render(
        request,
        'ecom_app/home.html',
        {
            'featured_products': featured_products,
            'category_products': category_products,  # New context variable
        }
    )

from django.db.models import Q
from .models import Product

def search_product(request):
    query = request.GET.get('q')

    products = Product.objects.filter(
        Q(title__icontains=query) |
        # Q(description__icontains=query) |
        Q(category__icontains=query)
        # Q(brand__icontains=query)
    )

    return render(
        request,
        'ecom_app/search.html',
        {
            'products': products,
            'query': query
        }
    )
def products(request):

    product = Product.objects.all()

    categories = request.GET.getlist('category')

    if categories:
        product = product.filter(category__in=categories)

    return render(
        request,
        'ecom_app/products.html',
        {'product': product}
    )



def electronic(request):
    product_list = Product.objects.filter(category='Electronics').order_by('-id')

    paginator = Paginator(product_list, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/electronic.html', {
        'page_obj': page_obj
    })

def appliance(request):
    product_list = Product.objects.filter(category='Home Appliances').order_by('-id')

    paginator = Paginator(product_list, 8)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/appliance.html', {
        'page_obj': page_obj
    })

def gaming(request):
    product_list = Product.objects.filter(category='Gaming').order_by('-id')

    paginator = Paginator(product_list, 8)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/gaming.html', {
        'page_obj': page_obj
    })

def fashion(request):
    product_list = Product.objects.filter(category='Fashion').order_by('-id')

    paginator = Paginator(product_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/fashion.html', {
        'page_obj': page_obj
    })

def accessories(request):
    product_list = Product.objects.filter(category='Accessories').order_by('-id')

    paginator = Paginator(product_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/accessories.html', {
        'page_obj': page_obj
    })

def beauty(request):
    product_list = Product.objects.filter(category='Beauty').order_by('-id')

    paginator = Paginator(product_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecom_app/beauty.html', {
        'page_obj': page_obj
    })

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

# @login_required(login_url='login')
# def profile(request):

#     profile = Customer.objects.filter(user=request.user).first()
#     print("hello kjdfksjdkfj sdfjdskjfksdjfksdjfkjds")
#     # POST request handle karo pehle
#     if request.method == "POST":
#         form = CustomerProfileForm(request.POST, request.FILES, instance=profile)

#         print("POST HIT ")

#         if form.is_valid():
#             data = form.save(commit=False)
#             data.user = request.user
#             data.save()

#             print("DATA SAVED ")


#             return redirect("profile2")   # ✔ correct

#         else:
#             print("ERROR:", form.errors)

#     else:
#         form = CustomerProfileForm(instance=profile)

#     return render(request,'ecom_app/profile.html', {'form': form,})

def profile(request):

    profile = Customer.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()

            # Redirect based on user type
            if data.user_type == 'admin':
                return redirect('admin_dashboard')  # ya admin_dashboard

            return redirect('home')  # customer

        else:
            print("ERROR:", form.errors)

    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'ecom_app/profile.html', {'form': form})


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

    # customer profile
    profile = Customer.objects.filter(user=user).first()

    # 🔥 session data
    buy_now_data = request.session.get('buy_now')

    cart_items = []
    total_amount = 0

    # =========================
    # 🔥 BUY NOW CASE
    # =========================
    if buy_now_data:
        try:
            product = Product.objects.get(id=buy_now_data['product_id'])
            quantity = buy_now_data.get('quantity', 1)

            cart_items = [{
                'product': product,
                'quantity': quantity
            }]

            total_amount = product.discounted_price * quantity

        except Product.DoesNotExist:
            cart_items = []
            total_amount = 0

    # =========================
    # 🔥 CART CASE
    # =========================
    else:
        cart_items_qs = Cart.objects.filter(user=user)

        for item in cart_items_qs:
            # IMPORTANT: always use discounted_price
            total_amount += item.product.discounted_price * item.quantity

        cart_items = cart_items_qs

    # =========================
    # 🔥 Razorpay Order
    # =========================
    import razorpay
    from django.conf import settings

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        "amount": int(total_amount * 100),  # paise conversion
        "currency": "INR",
        "payment_capture": "1"
    })

    # =========================
    # 🔥 IMPORTANT FIX (session cleanup)
    # =========================
    if 'buy_now' in request.session and not buy_now_data:
        del request.session['buy_now']

    return render(request, 'ecom_app/checkout.html', {
        'profile': profile,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # or dashboard
        else:
            return render(request, 'ecom_app/login.html', {
                'error': 'Invalid credentials'
            })

    # 🔥 THIS WAS MISSING
    return render(request, 'ecom_app/login.html')

# from .models import Customer

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is not None:
#             login(request, user)

#             try:
#                 customer = Customer.objects.get(user=user)

#                 if customer.user_type in ['seller', 'admin']:
#                     return redirect('admin_dashboard')

#             except Customer.DoesNotExist:
#                 pass

#             return redirect('home')

#         else:
#             messages.error(request, "Invalid Username or Password")

#     return render(request, 'ecom_app/login.html')


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

        #  cart clear
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
    print("VIEW HIT")
    if request.method == 'POST':
        print("POST HIT")
        email = request.POST.get('email')
        print("EMAIL =", email)
        try:
            user = User.objects.get(email=email)

            request.session['reset_user'] = user.id
            # request.session.modified = True
            # return redirect('reset_password')

            # OTP Generate
            otp = random.randint(100000,999999)

            # Session me store
            request.session['otp'] = str(otp)
            request.session['reset_email'] = email

            # Email Send
            send_mail(
                "Password Reset OTP",f"Your OTP is {otp}",
                "yourgmail@gmail.com",
                [email],
                fail_silently=False
            )

            return redirect('verify_otp')
        # except User.DoesNotExist:
        #     messages.error(request, 'No user with this email.')


        except User.DoesNotExist:
            messages.error(request,"Email not registered")

    return render(request, 'ecom_app/forgot_password.html')


def verify_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")
        saved_otp = request.session.get("otp")
        print("USER OTP =", user_otp)
        print("SESSION OTP =", saved_otp)

        if user_otp == saved_otp:
            print("OTP MATCH")
            return redirect("password_reset")

        else:
            print("OTP NOT MATCH")
            messages.error(request, "Invalid OTP")

    return render(request, "ecom_app/verify_otp.html")


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

# clsss userAdmin(apiviews):
#     def get():
#         obj=dfkdsj.objects.all()
#         obj=CustomerSerializer(obj,many=True)
#         return respo(obj.data)

#         pass
#     def post():
#         pass
#     def delete():
#         pass
#     def update():
#        PASS
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

class CartAdminViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .models import Customer, OrderPlaced


class UserAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):

        data = []

        for user in User.objects.all():

            orders = OrderPlaced.objects.filter(user=user)

            data.append({
                "user_id": user.id,
                "username": user.username,
                "total_orders": orders.count(),
                "delivered_orders": orders.filter(status="Delivered").count(),
                "pending_orders": orders.filter(status="Pending").count(),
                "cancelled_orders": orders.filter(status="Cancelled").count(),
            })

        return Response(data)

    def retrieve(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=404
            )

        customer = Customer.objects.filter(user=user).first()

        orders = OrderPlaced.objects.filter(user=user)

        product_details = []

        total_quantity = 0

        for order in orders:

            total_quantity += order.quantity

            product_details.append({
                "order_id": order.id,
                "product_id": order.product.id,
                "product_name": order.product.title,
                "quantity": order.quantity,
                "price": order.product.discounted_price,
                "status": order.status
            })

        data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },

            "customer": {
                "name": customer.name if customer else None,
                "city": customer.city if customer else None,
                "state": customer.state if customer else None,
                "locality": customer.locality if customer else None
            },

            "summary": {
                "total_orders": orders.count(),
                "total_products_purchased": total_quantity,
                "delivered_orders": orders.filter(
                    status="Delivered"
                ).count(),

                "pending_orders": orders.filter(
                    status="Pending"
                ).count(),

                "cancelled_orders": orders.filter(
                    status="Cancelled"
                ).count()
            },

            "products": product_details
        }

        return Response(data)
    

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, OrderPlaced
from django.db.models import Q

def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    # ── COUNTS ──
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = OrderPlaced.objects.count()

    
    query = request.GET.get('q')

    # ── LIST DATA ──
    recent_orders = OrderPlaced.objects.select_related('user', 'product').order_by('-id')[:10]
    all_orders = OrderPlaced.objects.select_related('user', 'product').order_by('-id')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()

    all_users = User.objects.all()

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,

        'recent_orders': recent_orders,
        'all_orders': all_orders,
        'products': products,
        'all_users': all_users,
    }

    return render(request, 'ecom_app/dashboard.html', context)

from django.shortcuts import render, redirect
from .models import Product

def add_product(request):

    if request.method == "POST":

        Product.objects.create(
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            brand=request.POST.get('brand'),
            selling_price=request.POST.get('selling_price'),
            discounted_price=request.POST.get('discounted_price'),
            product_image=request.FILES.get('product_image')
        )

        return redirect('admin_dashboard')

    return render(request,'ecom_app/add_product.html')

@login_required
@user_passes_test(is_admin)
def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.title = request.POST['title']
        product.category = request.POST['category']
        product.brand = request.POST['brand']
        product.selling_price = request.POST['selling_price']
        product.discounted_price = request.POST['discounted_price']
        if request.FILES.get('product_image'):
            product.product_image = request.FILES['product_image']
        product.save()
        return redirect('admin_dashboard')
    return render(request, 'ecom_app/edit_product.html', {'product': product})


def confirm_delete(request):
    return render(request, 'ecom_app/confirm_delete.html')



# import os
# from django.conf import settings

# @login_required
# @user_passes_test(is_admin)
# def delete_product(request, id):
#     product = get_object_or_404(Product, id=id)
    
#     # 🖼️ Image delete karo agar hai
#     if product.product_image:
#         try:
#             # Image ka path lo
#             image_path = os.path.join(settings.MEDIA_ROOT, str(product.product_image))
            
#             # Agar image exist karti hai toh delete karo
#             if os.path.isfile(image_path):
#                 os.remove(image_path)
#         except:
#             pass  # Agar image nahi hai toh kuch mat karo
    
#     # 📦 Product delete karo
#     product.delete()
    
#     messages.success(request, f'✅ "{product.title}" deleted successfully!')
#     return redirect('admin_dashboard')

import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import Product

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'role') and user.role == 'admin')

# ── DELETE PRODUCT WITH CONFIRMATION ──
@login_required
@user_passes_test(is_admin)
@transaction.atomic
def delete_product(request, id):
    """
    Delete product with confirmation page
    """
    product = get_object_or_404(Product, id=id)
    
    # GET request - Show confirmation page
    if request.method == 'GET':
        context = {
            'product': product,
            'total_products': Product.objects.count(),
            'related_orders': OrderPlaced.objects.filter(product=product).count(),  # Agar orders related hain
        }
        return render(request, 'ecom_app/confirm_delete.html', context)
    
    # POST request - Actually delete the product
    if request.method == 'POST':
        confirm = request.POST.get('confirm', 'false')
        
        if confirm == 'true':
            try:
                product_title = product.title
                
                # 🖼️ Delete image file
                if product.product_image:
                    try:
                        # Multiple ways to get image path
                        if hasattr(product.product_image, 'path'):
                            image_path = product.product_image.path
                        else:
                            image_path = os.path.join(settings.MEDIA_ROOT, str(product.product_image))
                        
                        if os.path.isfile(image_path):
                            os.remove(image_path)
                            print(f"✅ Image deleted: {image_path}")
                    except Exception as e:
                        print(f"⚠️ Error deleting image: {e}")
                
                # 📦 Delete product from database
                product.delete()
                
                messages.success(request, f'✅ "{product_title}" deleted successfully!')
                return redirect('admin_dashboard')
                
            except Exception as e:
                messages.error(request, f'❌ Error deleting product: {str(e)}')
                return redirect('admin_dashboard')
        else:
            messages.warning(request, '⚠️ Deletion cancelled!')
            return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')
