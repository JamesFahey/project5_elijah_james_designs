from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.views import generic, View
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from profiles.models import UserProfile

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
        if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) | Q(description__icontains=query)
                )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


class ProductDetail(View):

    def get(self, request, product_id, *args, **kwargs):
        """ A view to show individual product details """

        product = get_object_or_404(Product, pk=product_id)
        reviews = product.reviews.order_by("date_added")

        # if request.user.is_authenticated:
        #     user_profile = get_object_or_404(UserProfile, user=request.user)

        favourite = False
        if product.favourite.filter(id=request.user.id).exists():
            favourite = True

        context = {
            'product': product,
            'favourite': favourite,
            "reviews": reviews,
            "review_form": ReviewForm()
        }

        return render(request, 'products/product_detail.html', context)

    def post(self, request, product_id, *args, **kwargs):
        """ Add a review to a product """

        product = get_object_or_404(Product, pk=product_id)
        reviews = product.reviews.order_by("date_added")

        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Successfully added review!')

        else:
            review_form = ReviewForm()
            messages.error(
                request,
                'Failed to add review. Please ensure the form is valid.')

        favourite = False
        if product.favourite.filter(id=request.user.id).exists():
            favourite = True

        return render(
            request,
            "products/product_detail.html",
            {
                "product": product,
                "favourite": favourite,
                "reviews": reviews,
                "reviewed": True,
                "review_form": ReviewForm()
            },
        )


def favourite_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.POST:
        if product.favourite.filter(id=request.user.id).exists():
            product.favourite.remove(request.user)
            messages.success(
                request, f'Removed {product.name} from your favourites'
                )
        else:
            product.favourite.add(request.user)
            messages.success(
                request, f'Added {product.name} to your favourites'
                )
        return HttpResponseRedirect(
            reverse('product_detail', args=[product.id]))

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
