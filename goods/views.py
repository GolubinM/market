from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models    import Price, Goods, Order, FavoritesStatuses, CompareStatuses, Discount
from .forms import CreateGoodsForm, SetPrice, GoodsCategoriesRadio, DiscountForm
from django.db.models import Sum

# для хранения промежуточных значений формы фильтра User при перезагрузке страницы
USER_FILTER_VALUES = [None, None,
                      'sort_by_category']


def goods_page(request):
    user = request.user
    print(user)
    goods = Goods.objects.all()
    cart_quantity = "пусто"
    cart = ""
    favorites = ""
    to_compare = ""
    if request.user.is_authenticated:
        if "favorites_only" in request.POST:
            goods = user.goods_set.all()
        favorites = user.goods_set.all()
        to_compare = user.compare_goods_set.all()
        quantity = get_cart_info(request).aggregate(Sum("count"))["count__sum"]
        if quantity:
            cart_quantity = f'{quantity} шт'
        cart = Goods.objects.filter(ordered=user)
    if not user.is_authenticated or not USER_FILTER_VALUES[1] == request.user or "clear_filter" in request.POST:
        USER_FILTER_VALUES[0] = None
        USER_FILTER_VALUES[2] = "sort_by_category"
    if "first-high-price" in request.POST:
        # print("set high price")
        USER_FILTER_VALUES[2] = "high_first"
    if "first-low-price" in request.POST:
        # print("set high price")
        USER_FILTER_VALUES[2] = "low_first"
    if "set_filter" in request.POST:
        form_category = GoodsCategoriesRadio(request.POST)
        if form_category.is_valid():
            USER_FILTER_VALUES[0] = form_category.cleaned_data
            # USER_FILTER_VALUES[1] = request.user
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
               'cart': cart,
               }
    return render(request, 'goods/goods.html', context)


def add_to_cart(request, pk):
    add_count(request, pk)
    return redirect('goods')


def favorites_status_change(request, pk):
    referer_page = request.META['HTTP_REFERER']
    user = request.user
    good = Goods.objects.get(pk=pk)
    status = user.goods_set.filter(pk=pk)
    if status:
        # print("В избранном присутствует, удаляем из избранного:")
        favs_good = FavoritesStatuses.objects.get(user=user, goods=good)
        print(favs_good)
        favs_good.delete()
    else:
        favs_good = FavoritesStatuses(user=user, goods=good)
        favs_good.save()
        # print("В избранном отсутствует, добавляем в избранное:")
    if 'compare-goods' in referer_page:
        # print('переход с compare-goods')
        return redirect('compare-goods')
    return redirect('goods')


@login_required(login_url="/login")
def compare_status_change(request, pk):
    user = request.user
    good = Goods.objects.get(pk=pk)
    status = user.compare_goods_set.filter(pk=pk)
    if status:
        favs_good = CompareStatuses.objects.get(user=user, goods=good)
        favs_good.delete()
    else:
        favs_good = CompareStatuses(user=user, goods=good)
        favs_good.save()
    return redirect('goods')


@login_required(login_url="/login")
def compare_goods(request, sort_by=None):
    print(sort_by)
    user = request.user
    goods_to_compare = user.compare_goods_set.all()
    cart = Order.objects.filter(client_id=request.user)
    goods_id_list_in_cart = cart.values_list('good_id', flat=True)
    if goods_to_compare:
        if sort_by == "title":
            sort_rule = ["title", "category", "current_price"]
        elif sort_by == "-title":
            sort_rule = ["-title", "category", "current_price"]
        elif sort_by == 'category':
            sort_rule = ["category", "title", "current_price"]
        elif sort_by == '-category':
            sort_rule = ["-category", "title", "current_price"]
        elif sort_by == 'price':
            sort_rule = ["current_price", "category", "title"]
        elif sort_by == '-price':
            sort_rule = ["-current_price", "category", "title"]
        else:
            sort_rule = ["title"]
        favorites = user.goods_set.all()
        context = {'goods_to_compare': goods_to_compare.order_by(*sort_rule),
                   'favorites': favorites,
                   'cart': cart,
                   'goods_id_list_in_cart': goods_id_list_in_cart,
                   }
        return render(request, 'goods/compare-goods.html', context)
    return redirect('goods')


@login_required(login_url="/login")
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
    if request.method == 'GET':
        return render(request, 'goods/viewgood.html', {'good': good, 'form': form})
    else:
        try:
            form = CreateGoodsForm(request.POST, instance=good)
            gd = form.save()
            last_price = Price.objects.filter(good_id=pk).order_by('-date_time_actual').first()
            print(last_price)
            # Если цена в карточке не изменилась, не добавляем новую запись в справочник цен
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
def set_price(request):
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


def check_for_discount(order):
    sum_for_one_client = 0
    all_ord = Order.objects.filter(client_id=order.client_id)
    for sum_ord in all_ord:
        sum_for_one_client += sum_ord.line_total()
    # поверяем каждую строку заказа на участие в каждой действующей программе скидок
    active_discounts = Discount.objects.filter(is_active=True)
    summ_with_discount = order.line_total()
    print(order.good_id, order.good_id.category)
    for discount in active_discounts:
        if discount.for_category and order.good_id.category == discount.for_category:
            summ_with_discount = order.line_total() * discount.size_in_percent
        if discount.for_goods == order.good_id or discount.is_for_every:
            summ_with_discount = order.line_total() * discount.size_in_percent
        if discount.for_each_numbers:
            count_for_apply_discount = order.count // discount.for_each_numbers
            summ_with_discount = order.line_total() - count_for_apply_discount * order.price * (
                    1 - discount.size_in_percent)
        if discount.min_order_sum and (sum_for_one_client >= discount.min_order_sum):
            summ_with_discount = summ_with_discount * discount.size_in_percent
    return round(summ_with_discount, 2)


@login_required(login_url="/login")
def cart_view(request):
    cart = Order.objects.filter(client_id=request.user)
    order_sum = 0
    order_with_discount_sum = 0
    for order in cart:
        order_sum += order.price * order.count
        order.with_discount_total = check_for_discount(order)
        order_with_discount_sum += order.with_discount_total
    context = {
        "cart": cart,
        "order_sum": order_sum,
        "order_with_discount_sum": order_with_discount_sum,
    }
    return render(request, 'goods/cart-view.html', context)


@login_required(login_url="/login")
def get_cart_info(request):
    user = request.user
    cart_user = Order.objects.filter(client_id=user)
    return cart_user


@login_required(login_url="/login")
def substract_count(request, pk):
    client_id = request.user
    try:
        same_good_in_order = Order.objects.get(good_id=pk, client_id=client_id)
        if same_good_in_order.count > 0:
            same_good_in_order.count = same_good_in_order.count - 1
            same_good_in_order.save()
    except Exception as e:
        print("Ошибка получения строки заказа", e)
    referer_page = request.META['HTTP_REFERER']
    if 'compare-goods' in referer_page:
        return redirect('compare-goods')
    elif 'cart-view' in referer_page:
        return redirect('cart_view')


@login_required(login_url="/login")
def add_count(request, pk):
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
    referer_page = request.META['HTTP_REFERER']
    if 'compare-goods' in referer_page:
        return redirect('compare-goods')
    elif 'cart-view' in referer_page:
        return redirect('cart_view')


@login_required(login_url="/login")
def delete_order_row(request, pk, from_form=True):
    client_id = request.user
    try:
        Order.objects.filter(good_id=pk, client_id=client_id).delete()
    except Exception as e:
        print("Ошибка удаления строки заказа", e)
    if from_form:
        return redirect('cart_view')


@login_required(login_url="/login")
def clear_order(request):
    client_id = request.user
    try:
        Order.objects.filter(client_id=client_id).delete()
    except Exception as e:
        print("Ошибка очистки корзины", e)
    return redirect('goods')


@staff_member_required
def discounts_manage(request):
    discounts = Discount.objects.all().order_by('-is_active')
    context = {
        'title': "Управление скидками:",
        'discounts': discounts
    }
    return render(request, 'goods/discounts-manage.html', context)


@staff_member_required
def delete_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    discount.delete()
    return redirect('discounts-manage')


@staff_member_required
def edit_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    form = DiscountForm(instance=discount)
    if request.method == 'GET':
        return render(request, 'goods/discount.html', {'discount': discount, 'form': form})
    else:
        try:
            form = DiscountForm(request.POST, instance=discount).save()
            return redirect('discounts-manage')
        except ValueError as e:
            print(e)
            return render(request, 'goods/edit-discount.html',
                          {'discount': discount, 'form': form, 'error': 'Неверные данные!'})


def discounts(request):
    active_discount = Discount.objects.filter(is_active=True)
    discount_info = ''
    for discount in active_discount:
        discount_info += f"🍁 {discount.description}<br>"
    context = {
        'title': "Информация о действующих скидках:",
        'content': discount_info

    }
    return render(request, 'seller/home.html', context)


def add_discount(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discounts-manage')
    else:
        form = DiscountForm()
        return render(request, 'goods/discount.html', {'form': form})
