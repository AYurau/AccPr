import json
import datetime
import os

from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .excel import read_order, remains_model, delete_products, create_report
from .forms import Auth
from .models import Product


def index(request):
    return render(request, 'main/index.html')


def main(request):
    products = Product.objects.all()
    return render(request, 'main/main.html', {'products': products})


def remains(request):
    products = Product.objects.all()
    return render(request, 'main/remains.html', {'products': products})


def add(request):
    if request.method == "POST":
        order = request.FILES["order"]
        fs = FileSystemStorage()
        fs.save('order.xlsx', order)
        print('Успешно [Заявка]')
        read_order()
    return render(request, 'main/add.html')


# def invoice(request):
#   if request.method == "POST":
#      file = request.FILES['invoice']
#     fs = FileSystemStorage()
#    fs.save('ttn.xlsx',file)
#   print('Успешно [накладная]')
#  invoice_check()
# return render(request, 'main/index.html')
# else:
#    return render(request, 'main/add_n.html')


def reports(request):
    delete_products()
    return render(request, 'main/reports.html')


def result(request):
    return render(request, 'main/send.php')


def check_code(request):
    products_in_base = Product.objects.all()
    if request.GET['code'] == 'Ok':
        print(request.GET['code'])
        return HttpResponse({'a': 1}, headers={
            'Content-Type': 'application/json'
        })
    else:
        code = request.GET['code']
        for note in products_in_base:
            if code == note.code:
                note.count = note.count - 1
                note.save()
                if note.count == 0:
                    note.delete()
                return JsonResponse({
                    'success': {
                        'code': code,
                        'price': note.cost_fs,
                        'purchase': note.cost_m,
                        'name': note.title,
                        'amount': 1
                    }
                })


def products_recipets(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    products = body['products']
    paymentType = body['paymentType']
    for items in products:
        print(items['name'])
    print(paymentType)
    create_dir(products,paymentType)
    return JsonResponse({'success': {'message': 'saved'}})


def create_dir(products, paymentType):
    current_date = datetime.date.today()
    month = int(current_date.month)
    DIR_NAME = ''
    if month == 1:
        DIR_NAME = 'Январь'
    elif month == 2:
        DIR_NAME = 'Февраль'
    elif month == 3:
        DIR_NAME = 'Март'
    elif month == 4:
        DIR_NAME = 'Апрель'
    elif month == 5:
        DIR_NAME = 'Май'
    elif month == 6:
        DIR_NAME = 'Июнь'
    elif month == 7:
        DIR_NAME = 'Июль'
    elif month == 8:
        DIR_NAME = 'Август'
    elif month == 9:
        DIR_NAME = 'Сентябрь'
    elif month == 10:
        DIR_NAME = 'Октябрь'
    elif month == 11:
        DIR_NAME = 'Ноябрь'
    elif month == 12:
        DIR_NAME = 'Декабрь'
    try:
        os.mkdir('files/'+DIR_NAME)
    except OSError:
        print('Существует')
    create_report(products,paymentType,current_date,DIR_NAME)



# Create your views here.
class AuthUser(LoginView):
    template_name = 'index.html'
    form_class = Auth
    success_url = reverse_lazy('index')
