
from .cart import Cart

def cart(request):
    
    return {'cart': Cart(request)}

#Using context_processor to make the cart available throughout the application





