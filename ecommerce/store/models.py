from django.db import models

from django.urls import reverse
# Create your models here.

class Category(models.Model):
    
    name = models.CharField(max_length=250, db_index=True) #db_index: reading the database and stop whenever it found the attribute not reading the entire database model
    
    slug = models.SlugField(max_length=250, unique=True) #Make the category going to be unique
    
    class Meta:
        
        verbose_name_plural = 'categories' #override admin default 's' 
        
    # Admin model default register from Category(1), Category(2) to Category(name), ...
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        
        return reverse('list-category', args=[self.slug]) #dynamics URL    
    
class Product(models.Model):
    #Foreign key to link the products to a category
    #FK
    # on_delete=models.CASCADE If once a category is removed, for instance, those products will be removed automatically
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null = True)
    
    
    title = models.CharField(max_length=250)
    
    brand = models.CharField(max_length=250, default = 'un-branded')
    
    description = models.TextField(blank=True)
    
    slug = models.SlugField(max_length=250) #Make the Product  going to be unique
    
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    image = models.ImageField(upload_to='images/') #Upload image to the static/media/images folder
    
    class Meta:
        
        verbose_name_plural = 'products' #override admin default 's' 
        
    # Admin page default register from Product(1), Product(2) to Product(title), ...
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        
        return reverse('product-info', args=[self.slug]) #dynamics URL 
    

