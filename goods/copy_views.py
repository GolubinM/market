from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
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
    prices = Price.objects.filter(good_id=pk)
    form = CreateGoodsForm(instance=good)
    last_price = Price.objects.filter(good_id=pk).order_by('-date_time_actual').first()
    price_form = SetPrice(instance=last_price)
    if request.method == 'GET':
        return render(request, 'goods/viewgood.html',
                      {'good': good, 'prices': prices, 'form': form, 'price_form': price_form})
    else:
        try:
            form = CreateGoodsForm(request.POST, instance=good)
            price_form = SetPrice(request.POST, instance=last_price)
            gd = form.save()
            print(gd.pk)
            pr = price_form.save(commit=False)
            pr.good_id = gd.pk
            pr.save()
            return redirect('goods')
        except ValueError:
            return render(request, 'goods/viewgood.html',
                          {'form': form, 'error': 'Неверные данные!', 'prices': prices, 'price_form': price_form})


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
