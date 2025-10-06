from django.shortcuts import render, redirect
from .models import NewsCategory, News
from .forms import RegForm, AddForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View


# Create your views here.
def home_page(request):
    # Достаём всё из БД
    categories = NewsCategory.objects.all()
    news = News.objects.all()

    # Передаём данные на Frontend
    context = {
        'categories': categories,
        'news': news
    }
    return render(request, 'home.html', context)


# Страница выбора категории
def category_page(request, pk):
    # Достаём данные из БД
    category = NewsCategory.objects.get(id=pk)
    news = News.objects.filter(news_category=category)
    # Передаём данные на Frontend
    context = {
        'category': category,
        'news': news
    }
    return render(request, 'category.html', context)

# Страница выбранной новости
def news_page(request, pk):
    # Достаём данные из БД
    news = News.objects.get(id=pk)
    # Передаём данные на Frontend
    context = {
        'news': news
    }
    return render(request, 'news.html', context)

# Поиск товара по названию
def search(request):
    if request.method == "POST":
        # Достаём данные с формы
        get_news = request.POST.get("search_news")
        # Достаём данные из БД
        searched_news = News.objects.filter(news_title__icontains=get_news)
        if searched_news:
            context = {
                "news": searched_news,
                "request": get_news
            }
            return render(request, 'result.html', context)
        else:
            context = {
                "news": "",
                "request": get_news
            }
            return render(request, 'result.html', context)

# Регистрация
class Register(View):
    template_file = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}
        return render(request, self.template_file, context)

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def add_news(request):
    if request.method == "POST":
        added_news = AddForm(request.POST, request.FILES)
        if added_news.is_valid():
            added_news.save()
            return redirect('/')
    else:
        added_news = AddForm()

    context = {
        "news": added_news
    }
    return render(request, "add_news.html", context)


