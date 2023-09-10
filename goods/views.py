from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Price, Goods, Order
from .forms import CreateGoodsForm, SetPrice
from django.db.models import Sum, F


def goods_page(request):
    goods = Goods.objects.all()
    # user_pk = get_cart_info(request)
    if request.user.is_authenticated:
        quantity = get_cart_info(request).aggregate(Sum("count"))["count__sum"]
        if quantity:
            print(quantity)
            cart_quantity = f'{quantity} шт'
        else:
            cart_quantity = "пусто"

    else:
        cart_quantity = "пусто"
    # print(cart_quantity['count__sum'])

    return render(request, 'goods/goods.html', {"goods": goods, 'cart_quantity': cart_quantity})


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


def add_to_cart(request, pk):
    add_count(request, pk, call_from_template=False)
    return redirect('goods')


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
    print(call_from_template)
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
