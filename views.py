from django.contrib.auth import logout
from django.db.transaction import commit
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, CreateStatement,AddNews,CreateService
from django.contrib import messages, auth
from django.urls import reverse
import random
from django.utils import timezone
from .models import Statement,News, Services



def index(request):
    # Получаем текущую дату
    today = timezone.now().date()
    new = News.objects.filter(date=today).order_by('-id')
    services = Services.objects.all()
    return render(request, "index.html", {'new':new,'services':services})


def profile(request):
    if request.user.is_authenticated:
        history = request.user.statement_set.all().order_by('-date')[:6]
        history_count=history.count()
        # Получаем последнюю заявку пользователя
        try:
            statement = Statement.objects.filter(user=request.user).latest('id')
        except Statement.DoesNotExist:
            statement = None
        
        if request.method == 'POST' and 'avatar' in request.FILES:
            user = request.user
            user.avatar = request.FILES['avatar']
            user.save()
            return redirect('profile')
        
        return render(request, "profile.html", {
            'user': request.user,
            'stat': statement,
            'history': history,
            'count': history_count,
        })
    
    if request.method == 'POST':
        log = UserLoginForm(data=request.POST)
        if log.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('index')
    else:
        log = UserLoginForm()

    if request.method == 'POST':
        reg = UserRegistrationForm(request.POST)
        if reg.is_valid():
            user = reg.save(commit=False)
            user.save()
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('index')
    else:
        reg = UserRegistrationForm()

    if request.GET.get('data') != None:
        received_data = request.GET.get('data')
    else: 
        received_data = ''
    return render(request, "profile.html", {'log':log, 'reg':reg, 'received_data':received_data})


def log_out(request):
    logout(request)
    return redirect('profile')

def make_statement(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateStatement(request.POST)
            if form.is_valid():
                stat = form.save(commit=False)
                stat.user = request.user
                stat.save()
                return redirect('profile')
        else:
            form = CreateStatement()
            return render(request, 'application.html', {'application': form})
    else:
        some_data = f'Авторезуйтесь или Зарегестрируйтесь для подачи заявления'
        return redirect(reverse('profile') + f'?data={some_data}')
    
    return render(request,'application.html')

def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('index')  # Не суперпользователь → редирект

    stat = Statement.objects.all()
    form = CreateService()
    news_form = AddNews()

    if request.method == 'POST':
        # Обработка формы услуг
        if 'service_submit' in request.POST:
            form = CreateService(request.POST, request.FILES)
            if form.is_valid():
                service = form.save(commit=False)
                service.user = request.user
                service.save()
                return redirect('admin_panel')

        # Обработка формы новостей
        elif 'news_submit' in request.POST:
            news_form = AddNews(request.POST, request.FILES)
            if news_form.is_valid():
                news_item = news_form.save(commit=False)
                news_item.user = request.user
                news_item.save()
                return redirect('admin_panel')

    # Всегда возвращаем HttpResponse (рендер или редирект)
    return render(request, 'admin_panel.html', {
        'stat': stat,
        'form': form,
        'news': news_form,
    })

def deny(request):
    if request.method == 'POST':
        statement_id = request.POST.get('id')
        statement = Statement.objects.get(id=statement_id)
        statement.status = 'Отклонено'  # установите ваш статус
        statement.save()
        return redirect('admin_panel')  # замените на вашу страницу
    return redirect('admin_panel') # Метод не разрешен

def accept(request):
    if request.method == 'POST':
        statement_id = request.POST.get('id')
        statement = Statement.objects.get(id=statement_id)
        statement.status = 'Принято'
        statement.save()
        return redirect('admin_panel')
    return redirect('admin_panel')


def deleteService(request, service_id):
    ser = Services.objects.get(pk=service_id)
    if request.user.is_superuser:
        ser.delete()   
    return redirect('index')






























# def index(request):
#     if request.user.is_superuser:
#         return redirect('admin_panel')
#     if request.user.is_authenticated:
#         statements = Statement.objects.filter(user=request.user)
#         return render(request, 'index.html', {'user': request.user, 'stat': statements})
#     else:
#         return render(request, 'index.html')

# def make_statement(request):
#     if request.user.is_superuser:
#         return redirect('admin_panel')
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = CreateStatement(request.POST)
#             if form.is_valid():
#                 stat = form.save(commit=False)
#                 stat.user = request.user
#                 stat.unique_id = random.randint(1488, 9999)
#                 stat.save()
#                 return redirect('index')
#         else:
#             form = CreateStatement()
#             return render(request, 'make_stat.html', {'user': request.user, 'form': form})
#     else:
#         return redirect('index')

# def reg(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             messages.success(request, "Вы успешно зарегистрированы!")
#             return redirect('auth')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})


# def login(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return redirect('index')
#     else:
#         form = UserLoginForm()
#     return render(request, 'auth.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect('index')

# def admin_panel(request):
#     if request.user.is_superuser:
#         stat = Statement.objects.all()
#         return render(request, 'admin_panel.html', {'stat': stat, })
#     else:
#         return redirect('index')

# def deny(request):
#     if request.method == 'POST':
#         statement_id = request.POST.get('id')
#         statement = Statement.objects.get(id=statement_id)
#         statement.status = 'Отклонено'  # установите ваш статус
#         statement.save()
#         return redirect('admin_panel')  # замените на вашу страницу
#     return redirect('admin_panel') # Метод не разрешен

# def accept(request):
#     if request.method == 'POST':
#         statement_id = request.POST.get('id')
#         statement = Statement.objects.get(id=statement_id)
#         statement.status = 'Принято'
#         statement.save()
#         return redirect('admin_panel')
#     return redirect('admin_panel')
