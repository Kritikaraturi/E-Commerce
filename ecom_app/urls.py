from django.urls import path, reverse_lazy
from ecom_app.views import base, home, products, electronic, appliance, gaming, fashion, accessories, beauty, product_detail, RegistrationView, user_logout, profile, changepassworddone, add_to_cart, checkout, login_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PasswordChangeForm
from ecom_app import views
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, CartViewSet, OrderPlacedViewSet
from django.urls import path, include
# router = DefaultRouter()

# router.register(r'products', ProductViewSet)
# router.register(r'customers', CustomerViewSet)
# router.register(r'cart', CartViewSet)
# router.register(r'orders', OrderPlacedViewSet)

# urls.py

from rest_framework.routers import DefaultRouter
from .views import UserAdminViewSet, ProductAdminViewSet, CustomerAdminViewSet, OrderAdminViewSet, CartAdminViewSet, UserAnalyticsViewSet

router = DefaultRouter()    
router.register('admin/users', UserAdminViewSet)
router.register('admin/products', ProductAdminViewSet)
router.register('admin/customers', CustomerAdminViewSet)
router.register('admin/orders', OrderAdminViewSet)
router.register('admin/cart', CartAdminViewSet)
router.register('admin/user-analytics',UserAnalyticsViewSet, basename='user-analytics')

urlpatterns = router.urls

urlpatterns = [
    path('api/', include(router.urls)),
    path('base/', base, name='base'),
    path('home/', home, name='home'),
    path('search/', views.search_product, name='search'),
    path('products/', products, name='products'),
    path('electronic/', electronic, name='electronic'),
    path('appliance/', appliance, name='appliance'),
    path('gaming/', gaming, name='gaming'),
    path('fashion/', fashion, name='fashion'),
    path('accessories/', accessories, name='accessories'),
    path('beauty/', beauty, name='beauty'),
    path('product_detail/<int:product_id>', product_detail, name='product_detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/',views.login_view, name = "login"),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path("profile2/", views.get_curent_user_profile,name="profile2"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_view, name='cart'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='ecom_app/changepassword.html', form_class=PasswordChangeForm, success_url=reverse_lazy('passwordchangedone')), name='changepassword'),
    path('passwordchangedone/', changepassworddone, name='passwordchangedone'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('admin-dashboard/product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('admin-dashboard/product/add/', views.add_product,name='add_product'),
    path('admin-dashboard/product/confirm_delete/', views.confirm_delete,name='confirm_delete'),
    # path('update-profile/', views.update_profile, name='update_profile'),
    # path('change-password/', views.change_password, name='change_password'),


    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
