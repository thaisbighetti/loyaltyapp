"""loyaltyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from member.views import MemberList,  RegisterMember, MemberView, MainPage
from coupon.views import Generatecoupon, CouponList, CouponSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('register/', RegisterMember.as_view()),
    path('member/<str:cpf>', MemberView.as_view()),
    path('coupon/', Generatecoupon.as_view()),
    path('<str:cpf1>/coupon-to/<str:cpf2>', CouponList.as_view()),
    path('search/coupon/', CouponSearch.as_view()),
    path('search/member/', MemberList.as_view()),

]
