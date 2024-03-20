from decimal import Decimal
from store.models import Product

#Sessions handling


class Cart():
    def __init__(self, request):
        
        self.session = request.session
        
        #Returning user - obtain their existing session
        
        cart = self.session.get('session_key')
        
        #New user - generate a new session
        
        if 'session_key' not in request.session:
            
            cart = self.session['session_key'] = {}


        self.cart = cart
         
    def add(self, product, product_qty):
        
        product_id = str(product.id)
        
        if product_id in self.cart:
            
            self.cart[product_id]['qty'] = product_qty
            
        else:
            
            self.cart[product_id] = {'price':str(product.price), 'qty': product_qty}
            
        self.session.modified = True  
        
        
        


    def __len__(self):
        #.values()  method -> get the total number of items in the cart        
        return sum(item['qty'] for item in self.cart.values())
        # (item['qty'] for item in self.cart.values()) -> get all of the session data in the cart and add up total quantity of items in the card that we selected using sum() method

    def __iter__(self):
        
        all_product_ids = self.cart.keys() # get all of the product IDs of our products in the cart -> the product ID is a part of the cart key

        #select all of the products with the ID in the database, matches the IDs of what in our shopping cart
        
        products = Product.objects.filter(id__in=all_product_ids)
        
        #Copy an instance of the session data
        #cart = self.cart.copy()
        #Alternatively, deep copy the session data
        import copy
        
        cart =copy.deepcopy(self.cart)
        
        
        #Add some informations from the database for each matching product
        for product in products:
            
            cart[str(product.id)]['product'] = product

        
        #caculating total price for each items in our shopping cart
        for item in cart.values():
            #convert price from string to decimal
            item['price'] = Decimal(item['price'])
            #caculating the total cost of a item in our shopping cart
            item['total'] = item['price'] * item['qty']

            yield item


    #Caculate the total price in the shopping cart by looping through all item's total prices and calculate using sum()
    def get_total(self):

        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

        #return sum(Decimal(item['total']) for item in self.cart.values())
    
    
    def delete(self, product):
        
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True 
        
        
    def update(self, product, qty):
        product_id =str(product)
        
        product_quantity = qty
        
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity #overwrite the quantity
        
        self.session.modified = True 