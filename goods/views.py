from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CreateGoodsForm


def goods_page(request):
    goods = Goods.objects.all()
    return render(request, 'goods/goods.html', {"goods": goods})



def create_good(request):
    if request.method == 'POST':
        form = CreateGoodsForm(request.POST)
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
            form = CreateGoodsForm(request.POST,instance=good)
            form.save()
            return redirect('goods')
        except ValueError:
            return render(request, 'goods/viewgood.html', {'form': form, 'error': 'Неверные данные!'})
