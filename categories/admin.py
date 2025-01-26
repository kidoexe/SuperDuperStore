from django.contrib import admin
from categories.models import *

class CategoryImageInLines(admin.TabularInline):
    model = CategoryImage
    extra = 0

@admin.register(Category)
class PrdouctAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInLines]

    
