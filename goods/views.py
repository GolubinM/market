from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Price, Goods, Order
from .forms import CreateGoodsForm, SetPrice


def goods_page(request):
    goods = Goods.objects.all()
    return render(request, 'goods/goods.html', {"goods": goods})


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
            # Если цена в карточке не изменилась, не добавляем новую запись в справочник цен
            # print(last_price.price,gd.current_price, last_price.price==gd.current_price)
            if last_price.price != gd.current_price:
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
    goods = Goods.objects.all()
    return render(request, 'goods/goods.html', {"goods": goods})


def cart_view(request, client_id):
    cart = "cart request"
    # cart1 = Order.objects.filter(client_id=client_id)
    cart = Order.objects.all()
    print(cart)
    order_sum = 0
    for order_position in cart:
        order_sum += order_position.price * order_position.count
    context = {
        "cart": cart,
        "client_id": client_id,
        "order_sum": order_sum
    }
    return render(request, 'goods/cart-view.html', context)
