from django.shortcuts import render

from products.models import Product

# Create your views here.


def index(request):
    """ A view to return the index page """

    deals = Product.objects.filter(category_id=True)
    deals_length = len(deals)

    context = {
        'deals': deals,
        'deals_length': deals_length,
    }
    return render(request, 'home/index.html', context)
