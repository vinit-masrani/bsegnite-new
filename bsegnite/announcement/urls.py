from django.contrib import admin
from django.urls import re_path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
# from django.contrib.auth import views as auth_views
from .views import (
	post_announcement,
	post_chart,
	post_forgotpassword,
	post_login,
	post_register,
	post_tables,
	post_company_ann,
	post_company,
	post_logout,
	post_customize,
	dashboard,
    search_companies,
	# account_activation_sent,
	activate,
    aboutus,
	)



urlpatterns = [
    re_path(r'^$', post_announcement, name = 'home'),
    # re_path(r'forgotpassword/$',post_forgotpassword),
    re_path(r'password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'login/$',post_login,name='login'),
    re_path(r'logout/$',post_logout,name='logout'),
    re_path(r'register/$',post_register),
    re_path(r'tables/$',post_tables, name = 'tables'),
    re_path(r'company/(?P<cid>[\w.@+-]+)/$',post_company_ann, name = 'company_ann'),
    re_path(r'company/$',post_company, name = 'company'),
    re_path(r'customize/$',post_customize, name = 'customize'),
     re_path(r'dashboard/$',dashboard, name = 'dashboard'),
    # re_path(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    # re_path(r'^search/$',CompanyAutocomplete.as_view(), name='company-autocomplete',),
    re_path(r'^search/$',search_companies,),
    re_path(r'^about/$',aboutus,),

]
