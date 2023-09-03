from django.shortcuts import render
from .models import *
from .forms import CreateGoodsForm


def goods_page(request):
    goods = Goods.objects.all()
    return render(request, 'goods/goods.html', {"goods": goods})


# def project(request, model_id):
#     category_title = get_object_or_404(PaperModelsCategories, pk=model_id).title
#     project = PaperModels.objects.filter(category_id=model_id)
#     context = {"project": project,
#                "id": model_id,
#                "cat_title": category_title}
#     return render(request, 'papermodels/project.html', context=context)
#

def create_good(request):
    if request.method == 'POST':
        form = CreateGoodsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CreateGoodsForm()
    return render(request, 'goods/create-good.html', {'form': form})
