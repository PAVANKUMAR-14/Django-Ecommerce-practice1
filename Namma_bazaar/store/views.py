from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from store.models import product
from category.models import Category
from carts.models import cartItem
from carts.views import _cart_id

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category,slug=category_slug) #It will bring requested category
        products = product.objects.filter(category=categories, is_available=True)
         #It'll filter the products from above selected category
        paginators=Paginator(products,1)
        page=request.GET.get('page')
        page_product=paginators.get_page(page)
        product_count = products.count()
    else:
        products = product.objects.filter(is_available=True)
        product_count = products.count()
        paginators=Paginator(products,3)
        page=request.GET.get('page')
        page_product=paginators.get_page(page)

    context = {'products': page_product, 'product_count': product_count}

    return render(request, 'store/store.html', context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product=product.objects.get(category__slug=category_slug, slug=product_slug)
        incart=cartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()


    except Exception as e :
        raise e
    context={'single_product':single_product, 'incart':incart}

    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q (product_name__icontains=keyword))
    product_count = products.count()

                                                                
    context={'products':products,'product_count': product_count}

    return render (request,'store/store.html', context)

