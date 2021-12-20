from django.contrib import admin


from .models import Recommend


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['source', 'target', 'cupom', 'hoje', 'expires']
    list_filter = ('source', 'target',)
    list_display = ('source', 'target', 'cupom', 'hoje', 'expires')


admin.site.register(Recommend, CouponAdmin)
