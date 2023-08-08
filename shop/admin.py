from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')

admin.site.register(Catagory,CategoryAdmin)
admin.site.register(Product)