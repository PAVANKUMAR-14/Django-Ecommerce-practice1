from django.contrib import admin
from store.models import product,product_variation

# Register your models here.

class ProductAdmin (admin.ModelAdmin):
    list_display=['product_name','price','stocks','category','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(product,ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_name','is_active']
    list_filter=['product','variation_category','variation_name','is_active']
    list_editable=('is_active',)

admin.site.register(product_variation,VariationAdmin)



