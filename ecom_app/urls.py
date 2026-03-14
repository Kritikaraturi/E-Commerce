from django.urls import path
from ecom_app.views import base, home, products, electronic, appliance, gaming, fashion, accessories, beauty, product_detail, RegistrationView, user_logout, profile

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PasswordChangeForm


urlpatterns = [
    path('base/', base, name='base'),
    path('home/', home, name='home'),
    path('products/', products, name='products'),
    path('electronic/', electronic, name='electronic'),
    path('appliance/', appliance, name='appliance'),
    path('gaming/', gaming, name='gaming'),
    path('fashion/', fashion, name='fashion'),
    path('accessories/', accessories, name='accessories'),
    path('beauty/', beauty, name='beauty'),
    path('product_detail/<int:product_id>', product_detail, name='product_detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name = "ecom_app/login.html", authentication_form = LoginForm), name = "login"),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name = 'ecom_app/changepassword.html', form_class = PasswordChangeForm), name='changepassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
