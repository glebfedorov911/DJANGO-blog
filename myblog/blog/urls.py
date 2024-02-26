from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('newarticle/', views.CreateArticleView.as_view(), name='newarticle'),
    path('article/<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    path('article/<slug:article_slug>/edit/', views.ArticleEditView.as_view(), name='editarticle'),
    path('article/<slug:article_slug>/delete/', views.ArticleDeleteView.as_view(), name='deletearticle'),
    path('article/<slug:article_slug>/addcomm/', views.AddCommentView.as_view(), name='newcomment'),
]
