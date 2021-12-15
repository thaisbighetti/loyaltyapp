from django.contrib import admin
from .models import Member, RegisterMember

# Register your models here.
admin.site.register(Member)
admin.site.register(RegisterMember)

