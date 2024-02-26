from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.db.models import Q

from .backends import AuthBackend
from .forms import *

def index(request):
    return render(request, 'blog/index.html', {"us": request.user, "title": "index",
                                               "articles": Article.objects.all()})

class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = "blog/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            return redirect('index')
        except:
            return HttpResponse('error')

class LoginView(CreateView):
    form_class = LoginForm
    template_name = "blog/login.html"
    auth = AuthBackend()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context

    def post(self, *args, **kwargs):
        try:
            user = self.auth.authenticate(self.request, email=self.request.POST.get('phone'), password=self.request.POST.get('password'))

            if user:
                login(self.request, user)
            return redirect('index')
        except:
            return HttpResponse('error')

def log_out(request):
    try:
        logout(request)
        return redirect('index')
    except:
        return HttpResponse('error')

class CreateArticleView(CreateView):
    form_class = CreateArticleForm
    template_name = "blog/newarticle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание статьи"
        return context

    def post(self, *args, **kwargs):
        try:
            obj = Article.objects.create(
                name=self.request.POST.get('name'),
                desc=self.request.POST.get('desc'),
                img=self.request.FILES.get('img'),
                author=User.objects.get(id=self.request.user.id),
            )

            obj.save()

            return redirect('index')
        except:
            return HttpResponse('error')

class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Статья"
        context['comform'] = CreateCommentForm
        context['com'] = Comment.objects.all()
        return context


class ArticleEditView(UpdateView):
    model = Article
    template_name = "blog/editarticle.html"
    slug_url_kwarg = 'article_slug'
    form_class = CreateArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        return context

class ArticleDeleteView(DeleteView):
    model = Article
    slug_url_kwarg = 'article_slug'
    template_name = "blog/deletearticle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'
        return context

    def get(self, request, *args, **kwargs):
        instanse = Article.objects.filter(slug=kwargs.get('article_slug'))
        if not (instanse[0].author.id == request.user.id):
            return HttpResponse('error')

        try:
            instanse.delete()
            return redirect('index')
        except:
            return HttpResponse('error')

class AddCommentView(View):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Комментарий'
        return context

    def post(self, request, *args, **kwargs):
        try:
            Comment.objects.create(author=request.user, msg=request.POST.get('msg')).save()

            return redirect('article', kwargs.get('article_slug'))
        except:
            return HttpResponse('error')