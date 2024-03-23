from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404
# Create your views here.

def store(request):
    all_products = Product.objects.all()
    
    context = {
        'my_products': all_products,
    }
    
    return render(request, 'store/store.html', context)

def categories(request): # use for loop in the templates to automatically generate categories in dropdown menu at all pages (check base.html and setting file (context_processors))
    
    all_categories = Category.objects.all()
    
    return {'all_categories': all_categories}

def product_info(request, product_slug):
    
    product = get_object_or_404(Product, slug=product_slug) #checking if the slug at the url matches with the actual product's slug data 
    
    context = {'product': product}
    
    return render(request, 'store/product-info.html', context)


def list_category(request, category_slug=None):
    
    category = get_object_or_404(Category, slug=category_slug) #checking if the slug at the url matches with the actual category's slug data 
    
    products = Product.objects.filter(category=category) #check the product's foreign key with the actual searches category
    
    return render(request, 'store/list-category.html', {'category' : category, 'products': products}) 

def all_category(request):
    category = Category.objects.all()
    
    products = Product.objects.all()
    return render(request,'store/all_category.html',{'category' : category, 'products': products}) 


