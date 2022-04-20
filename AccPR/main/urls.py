from django.template.defaulttags import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('main.html', views.main),
    path('remains.html', views.remains),
    path('add.html', views.add),
    path('reports.html', views.reports),
    path('send.php', views.result),
    path('check_code/',views.check_code),
    path('products_receipt/',views.products_recipets)
]
