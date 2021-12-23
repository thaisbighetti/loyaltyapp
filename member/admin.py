from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    search_fields = ['cpf', 'name', 'created', 'email', 'phone', 'points']
    list_display = ('cpf', 'name', 'points', 'email', 'phone', 'created')


admin.site.register(Member, MemberAdmin)
