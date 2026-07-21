from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q  
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Category, Product, ProductImage


def home(request):
    """Asosiy sahifa"""
    user_id = request.session.get('user_id')
    current_user = User.objects.filter(id=user_id).first() if user_id else None

    categories = Category.objects.filter(is_active=True, parent=None)
    products = Product.objects.filter(is_active=True)
    
    return render(request, 'asosiy/home.html', {
        'categories': categories, 
        'products': products,
        'current_user': current_user
    })


def category_detail(request, category_id):
    """Kategoriya va filtrlash sahifasi"""
    category = get_object_or_404(Category, id=category_id, is_active=True)
    
    products = Product.objects.filter(category=category, is_active=True)
    
    search_query = request.GET.get('search', '').strip()
    location_query = request.GET.get('location', '').strip()
    price_from = request.GET.get('price_from', '').strip()
    price_to = request.GET.get('price_to', '').strip()
    condition = request.GET.get('condition', '').strip()

    if search_query:
        products = products.filter(Q(name_uz__icontains=search_query))
    
    if price_from and price_from.isdigit():
        products = products.filter(price__gte=int(price_from))
        
    if price_to and price_to.isdigit():
        products = products.filter(price__lte=int(price_to))

    if category.parent:
        sibling_categories = Category.objects.filter(parent=category.parent, is_active=True)
    else:
        sibling_categories = Category.objects.filter(parent=category, is_active=True)

    context = {
        'current_category': category,  
        'products': products,          
        'sibling_categories': sibling_categories,  
        'search_query': search_query,      
        'location_query': location_query,  
        'price_from': price_from,
        'price_to': price_to,
        'condition': condition,
    }
    return render(request, 'category_products/category_p.html', context)


def product_detail(request, product_id):
    """Mahsulotning batafsil sahifasi"""
    product = get_object_or_404(Product, pk=product_id)
    product_images = ProductImage.objects.filter(product=product)

    return render(request, 'asosiy/product_detail.html', {
        'product': product,
        'product_images': product_images
    })


def login_view(request):
    """Tizimga kirish"""
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = User.objects.filter(username=username_input).first()
        if not user:
            user = User.objects.filter(email=username_input).first()

        if user and check_password(password_input, user.password):
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return render(request, 'asosiy/login.html', {'error': 'Login yoki parol xato!'})

    return render(request, 'asosiy/login.html')


def register_view(request):
    """Ro'yxatdan o'tish"""
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'asosiy/register.html', {'error': 'Bu foydalanuvchi nomi allaqachon band!'})

        if phone and User.objects.filter(phone=phone).exists():
            return render(request, 'asosiy/register.html', {'error': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan!'})

        if password != confirm_password:
            return render(request, 'asosiy/register.html', {'error': 'Parollar bir-biriga mos kelmadi!'})

        user = User.objects.create(
            username=username, 
            email=email, 
            phone=phone,
            password=make_password(password)
        )

        request.session['user_id'] = user.id
        return redirect('home')

    return render(request, 'asosiy/register.html')


def logout_view(request):
    """Tizimdan chiqish"""
    request.session.flush()
    logout(request)
    return redirect('home')


def add_product(request):
    """Yangi e'lon qo'shish"""
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        name_uz = request.POST.get('name_uz')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        images = request.FILES.getlist('images')

        category = Category.objects.filter(id=category_id).first()
        current_user = User.objects.filter(id=user_id).first()

        # Birinchi rasm asosiy rasm bo'ladi
        product = Product.objects.create(
            name_uz=name_uz,
            price=price,
            category=category,
            phone=phone,
            location=location,
            user=current_user,
            image=images[0] if len(images) > 0 else None,
            is_active=True
        )

        # Galereya rasmlarini saqlaymiz
        for img in images:
            ProductImage.objects.create(
                product=product,
                image=img
            )

        return redirect('home')

    categories = Category.objects.filter(is_active=True)
    return render(request, 'asosiy/add_product.html', {'categories': categories})




# 1. TILNI ALMSHTIRISH (UZ / РУС)
def change_language(request, lang_code):
    request.session['django_language'] = lang_code
    # Sahifani kelgan joyiga qaytarish
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def account_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    user_products = Product.objects.filter(user=user).order_by('-id')
    total_products = user_products.count()

    return render(request, 'asosiy/account.html', {
        'profile_user': user,
        'user_products': user_products,
        'total_products': total_products
    })


# 3. CHAT SAHIFASI
def chat_view(request, receiver_id=None):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    current_user = get_object_or_404(User, id=user_id)
    
    # Suhbatdoshlar ro'yxatini olish
    sent_to = Message.objects.filter(sender=current_user).values_list('receiver_id', flat=True)
    received_from = Message.objects.filter(receiver=current_user).values_list('sender_id', flat=True)
    chat_user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=chat_user_ids)

    selected_user = None
    messages_list = []

    if receiver_id:
        selected_user = get_object_or_404(User, id=receiver_id)
        # Xabarlarni yuborish (POST)
        if request.method == 'POST':
            text = request.POST.get('message_text')
            if text:
                Message.objects.create(
                    sender=current_user,
                    receiver=selected_user,
                    text=text
                )
                return redirect('chat_with_user', receiver_id=receiver_id)

        # Muloqot xabarlarini olish
        messages_list = Message.objects.filter(
            (Q(sender=current_user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=current_user))
        ).order_by('created_at')

    return render(request, 'asosiy/chat.html', {
        'current_user': current_user,
        'chat_users': chat_users,
        'selected_user': selected_user,
        'messages_list': messages_list
    })