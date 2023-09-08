from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CreateGoodsForm, SetPrice


def goods_page(request):
    goods = Goods.objects.all()
    prices = Price.objects.all()
    return render(request, 'goods/goods.html', {"goods": goods, 'prices': prices})


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
    prices = Price.objects.filter(good_id=pk)
    last_price = prices.order_by('-date_time_actual').first()
    price_form = SetPrice(instance=last_price)

    if request.method == 'GET':
        return render(request, 'goods/viewgood.html', {'good': good, 'form': form, 'price_form': price_form})
    else:
        try:
            form = CreateGoodsForm(request.POST, instance=good)
            price_form = SetPrice(request.POST)
            gd = form.save()
            if last_price.price != float(request.POST.get("price")):
                pr = price_form.save(commit=False)
                pr.good_id = gd
                pr.save()

            return redirect('goods')
        except ValueError as e:
            print(e)
            return render(request, 'goods/viewgood.html',
                          {'good': good, 'form': form, 'price_form': price_form, 'error': 'Неверные данные!'})


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
