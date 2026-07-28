from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name_uz = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # <-- Xatolikni bartaraf etuvchi joy
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name_uz


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name_uz}"


class Message(models.Model):  # <-- Sintaksis to'g'rilandi
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.text[:20]}"