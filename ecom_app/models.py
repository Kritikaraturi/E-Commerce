from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', ' Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)
USER_TYPES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )

# class Customer(AbstractUser):
#     USER_TYPES = (
#         ('customer', 'Customer'),
#         ('seller', 'Seller'),
#     )
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     locality = models.CharField(max_length=200)
#     city = models.CharField(max_length=50)
#     state = models.CharField(choices=STATE_CHOICES, max_length=50)
#     profile_completed = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.id)


USER_TYPES = (
    ('customer', 'Customer'),
    ('seller', 'Seller'),
    ('admin', 'Admin'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='customer'
    )

    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
CATEGORY_CHOICES = (
    ('Accessories', 'Accessories'),
    ('Beauty', 'Beauty'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Gaming', 'Gaming'),
    ('Home Appliances', 'Home Appliances'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')


# from django.db import models

# class UserProfile(models.Model):
#     # General Settings
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True)
#     bio = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user_type = models.CharField(
#         max_length=20,
#         choices=USER_TYPES,
#         default='customer'
#     )
    
#     def __str__(self):
#         return f"{self.user.username}'s Profile"