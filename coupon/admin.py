from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['source', 'target', 'coupon', 'created', 'expires']
    list_filter = ('source', 'target',)
    list_display = ('source', 'target', 'coupon', 'created', 'expires')


admin.site.register(Coupon, CouponAdmin)
