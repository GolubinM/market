from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

import goods.models
from .models import Price, Goods, Order, FavoritesStatuses, CompareStatuses
from .forms import CreateGoodsForm, SetPrice, GoodsCategoriesRadio
from django.db.models import Sum, F

USER_FILTER_VALUES = [None, None,
                      'sort_by_category']  # для хранения промежуточных значений формы фильтра User при перезагрузке страницы


def goods_page(request):
    user = request.user
    goods = Goods.objects.all()
    if "favorites_only" in request.POST:
        goods = user.goods_set.all()

    favorites = user.goods_set.all()
    to_compare = user.compare_goods_set.all()
    cart_quantity = "пусто"
    if request.user.is_authenticated:
        quantity = get_cart_info(request).aggregate(Sum("count"))["count__sum"]
        if quantity:
            cart_quantity = f'{quantity} шт'

    if not user.is_authenticated or not USER_FILTER_VALUES[1] == request.user or "clear_filter" in request.POST:
        USER_FILTER_VALUES[0] = None
        USER_FILTER_VALUES[2] = "sort_by_category"

    if "first-high-price" in request.POST:
        print("set high price")
        USER_FILTER_VALUES[2] = "high_first"
    if "first-low-price" in request.POST:
        print("set high price")
        USER_FILTER_VALUES[2] = "low_first"

    if "set_filter" in request.POST:
        form_category = GoodsCategoriesRadio(request.POST)
        if form_category.is_valid():
            USER_FILTER_VALUES[0] = form_category.cleaned_data
            USER_FILTER_VALUES[1] = request.user
            data = form_category.cleaned_data
            selected_point = data['selected_categories']
            min_price_filter = data['min_price_filter']
            max_price_filter = data['max_price_filter']
            selected_id = [cat.id for cat in selected_point]
            goods = Goods.objects.filter(category__in=selected_id, current_price__gte=min_price_filter,
                                         current_price__lte=max_price_filter)
    else:
        if USER_FILTER_VALUES[0]:
            data = USER_FILTER_VALUES[0]
            selected_point = data['selected_categories']
            min_price_filter = data['min_price_filter']
            max_price_filter = data['max_price_filter']
            selected_id = [cat.id for cat in selected_point]
            goods = Goods.objects.filter(category__in=selected_id, current_price__gte=min_price_filter,
                                         current_price__lte=max_price_filter)
            form_category = GoodsCategoriesRadio(USER_FILTER_VALUES[0])
        else:
            form_category = GoodsCategoriesRadio()

    if USER_FILTER_VALUES[2] == "low_first":
        sort_rule = ["current_price", "category", "title"]
    elif USER_FILTER_VALUES[2] == 'high_first':
        sort_rule = ["-current_price", "category", "title"]
    else:
        sort_rule = ["category", "current_price", "title"]

    context = {"goods": goods.order_by(*sort_rule),
               'cart_quantity': cart_quantity,
               'form_category': form_category,
               'favorites': favorites,
               'to_compare': to_compare,
               }
    return render(request, 'goods/goods.html', context)


def add_to_cart(request, pk):
    add_count(request, pk, call_from_template=False)
    return redirect('goods')


def favorites_status_change(request, pk):
    referer_page = request.META['HTTP_REFERER']
    user = request.user
    good = Goods.objects.get(pk=pk)
    # print(good)
    # statuses = user.goods_set.all()
    # status = len(user.goods_set.filter(pk=pk))
    status = user.goods_set.filter(pk=pk)
    if status:
        print("В избранном присутствует, удаляем из избранного:")
        favs_good = FavoritesStatuses.objects.get(user=user, goods=good)
        print(favs_good)
        favs_good.delete()
    else:
        favs_good = FavoritesStatuses(user=user, goods=good)
        print(favs_good)
        favs_good.save()
        print("В избранном отсутствует, добавляем в избранное:")
    status = user.goods_set.filter(pk=pk)
    print(status)
    print("favorites status changed!!!")
    # add_count(request, pk, call_from_template=False)
    if 'compare-goods' in referer_page:
        # print('переход с compare-goods')
        return redirect('compare-goods')
    return redirect('goods')


def compare_status_change(request, pk):
    user = request.user
    good = Goods.objects.get(pk=pk)
    # print(good)
    # statuses = user.goods_set.all()
    # status = len(user.goods_set.filter(pk=pk))
    status = user.compare_goods_set.filter(pk=pk)
    if status:
        print("В сравнении присутствует, удаляем из избранного:")
        favs_good = CompareStatuses.objects.get(user=user, goods=good)
        print(favs_good)
        favs_good.delete()
    else:
        favs_good = CompareStatuses(user=user, goods=good)
        print(favs_good)
        favs_good.save()
        print("В сравнении отсутствует, добавляем в избранное:")
    status = user.compare_goods_set.filter(pk=pk)
    print(status)
    print("compare status changed!!!")
    # add_count(request, pk, call_from_template=False)
    return redirect('goods')


def compare_goods(request):
    user = request.user
    goods_to_compare = user.compare_goods_set.all()
    cart = Order.objects.filter(client_id=request.user)
    if goods_to_compare:
        favorites = user.goods_set.all()
        context = {'goods_to_compare': goods_to_compare,
                   'favorites': favorites,
                   'cart': cart,
                   }
        return render(request, 'goods/compare-goods.html', context)

    return redirect('goods')


def create_good(request):
    if request.method == 'POST':
        form = CreateGoodsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('goods')
    else:
        form = CreateGoodsForm()
        return render(request, 'goods/create-good.html', {'form': form})


@staff_member_required
def deletegood(request, pk):
    good = get_object_or_404(Goods, pk=pk)
    if request.method == "POST":
        good.delete()
        return redirect('goods')


@staff_member_required
def viewgood(request, pk):
    good = get_object_or_404(Goods, pk=pk)
    form = CreateGoodsForm(instance=good)
    # user_pk = request.user.pk

    if request.method == 'GET':
        return render(request, 'goods/viewgood.html', {'good': good, 'form': form})
    else:
        try:
            form = CreateGoodsForm(request.POST, instance=good)
            gd = form.save()
            last_price = Price.objects.filter(good_id=pk).order_by('-date_time_actual').first()
            print(last_price)
            # Если цена в карточке не изменилась, не добавляем новую запись в справочник цен
            # print(last_price.price,gd.current_price, last_price.price==gd.current_price)
            if last_price:
                if last_price.price != gd.current_price:
                    new_price = Price(price=gd.current_price, good_id=gd)
                    new_price.save()
            else:
                new_price = Price(price=gd.current_price, good_id=gd)
                new_price.save()

            return redirect('goods')
        except ValueError as e:
            print(e)
            return render(request, 'goods/viewgood.html',
                          {'good': good, 'form': form, 'error': 'Неверные данные!'})


@staff_member_required
def set_price(request, pk):
    price = get_object_or_404(Price, good_id=request.goods)
    form = SetPrice(instance=price)
    if request.method == 'GET':
        return render(request, 'goods/set-price.html', {'price': price, 'form': form})
    else:
        try:
            form = SetPrice(request.POST, instance=price)
            form.save()
            return redirect('goods')
        except ValueError:
            return render(request, 'goods/set-price.html', {'form': form, 'error': 'Неверные данные!'})


def cart_view(request):
    cart = Order.objects.filter(client_id=request.user)
    order_sum = 0
    for order_position in cart:
        order_sum += order_position.price * order_position.count
    # переделать функцию класса Order.line_total() в атрибут, цикл убрать
    # order_sum = cart.aggregate(Sum("line_total"))
    context = {
        "cart": cart,
        "order_sum": order_sum
    }
    return render(request, 'goods/cart-view.html', context)


def get_cart_info(request):
    user = request.user
    cart_user = Order.objects.filter(client_id=user)
    return cart_user


def substract_count(request, pk, from_form=True):
    client_id = request.user
    try:
        same_good_in_order = Order.objects.get(good_id=pk, client_id=client_id)
        if same_good_in_order.count > 0:
            same_good_in_order.count = same_good_in_order.count - 1
            same_good_in_order.save()
    except Exception as e:
        print("Ошибка получения строки заказа", e)
    if from_form:
        return redirect('cart_view')


def add_count(request, pk, call_from_template=True):
    gd = get_object_or_404(Goods, pk=pk)
    client_id = request.user
    try:
        same_good_in_order = Order.objects.get(good_id=pk, client_id=client_id)
        same_good_in_order.count = same_good_in_order.count + 1
        same_good_in_order.save()
    except Order.DoesNotExist:
        count = 1
        new_order_row = Order(client_id=client_id, price=gd.current_price, good_id=gd, count=count)
        new_order_row.save()
    # print(call_from_template)
    if call_from_template:
        return redirect('cart_view')


def delete_order_row(request, pk, from_form=True):
    client_id = request.user
    try:
        Order.objects.filter(good_id=pk, client_id=client_id).delete()
    except Exception as e:
        print("Ошибка удаления строки заказа", e)
    if from_form:
        return redirect('cart_view')


def clear_order(request):
    client_id = request.user
    try:
        Order.objects.filter(client_id=client_id).delete()
    except Exception as e:
        print("Ошибка очистки корзины", e)
    return redirect('goods')

# def category_select(request):
#     if request.method == 'POST':
#         form_category = GoodsCategoriesRadio(request.POST)
#         if form_category.is_valid():
#             seleted_point = form_category.cleaned_data['selected_categories']
#             for cat in seleted_point:
#                 print(cat)
#             print(form.cleaned_data)
#             profile.user = request.user
#             profile.save()
#             form.save_m2m()  # needed since using commit=False
#         else:
#             form = GoodsCategoriesRadio()
#     context = {'form_category': form_category}
#     return redirect('goods')
