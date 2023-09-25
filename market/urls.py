"""
URL configuration for market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from seller.views import *
from goods.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
    path("contacts/", contacts, name="contacts"),
    path("discounts/", discounts, name="discounts"),
    path("discounts-manage/", discounts_manage, name="discounts-manage"),
    path("add-discount/", add_discount, name="add-discount"),
    path("", home, name="home"),
    path("goods/", goods_page, name="goods"),
    path("create-good/", create_good, name="create-good"),
    path("viewgood/<int:pk>", viewgood, name="viewgood"),
    path("viewgood/<int:pk>/delete", deletegood, name="delete"),
    path("delete-discount/<int:pk>", delete_discount, name="delete-discount"),
    path("edit-discount/<int:pk>", edit_discount, name="edit-discount"),
    path("viewgood/<int:pk>/add_to_cart", add_to_cart, name="add_to_cart"),
    path("viewgood/<int:pk>/favorites-status-change", favorites_status_change, name="favorites-status-change"),
    path("viewgood/<int:pk>/compare-status-change", compare_status_change, name="compare-status-change"),
    path("cart-view/", cart_view, name="cart_view"),
    path("substract_count/<int:pk>", substract_count, name="substract_count"),
    path("add_count/<int:pk>", add_count, name="add_count"),
    path("delete_order_row/<int:pk>", delete_order_row, name="delete_order_row"),
    path("clear_order/", clear_order, name="clear_order"),
    path("compare-goods/", compare_goods, name="compare-goods"),
    path("compare-goods/<str:sort_by>", compare_goods, name="compare-goods"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
