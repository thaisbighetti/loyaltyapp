from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    search_fields = ['cpf', 'name', ]
    list_display = ('cpf', 'name',)


# Register your models here.
admin.site.register(Member, MemberAdmin)
