from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    home, category_detail, product_detail, login_view, 
    register_view, logout_view, add_product,
    change_language, account_profile, chat_view  
)

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-product/', add_product, name='add_product'),
    
    # Auth yo'llari
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # TIL VA FOYDALANUVCHI YO'LLARI
    path('lang/<str:lang_code>/', change_language, name='change_language'),
    path('account/', account_profile, name='account_profile'),
    path('chat/', chat_view, name='chat'),
    path('chat/<int:receiver_id>/', chat_view, name='chat_with_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)