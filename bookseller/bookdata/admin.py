from django.contrib import admin
from .models import Author, Publisher, Catagory, Catalog, Orderdetails
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Catagory)
admin.site.register(Catalog)
admin.site.register(Orderdetails)
# Register your models here.
