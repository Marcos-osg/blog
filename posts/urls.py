from django.urls import path
from posts import views as v


urlpatterns = [
    path('',v.PostIndex.as_view(), name='index'),
    path('categoria/<str:categoria>',v.PostCategoria.as_view(), name='post_categoria'),
    path('post/<int:pk>',v.PostDetalhes.as_view(), name='post_detalhes'),
    path('sobre/',v.sobre, name='sobre'),
    path('novo_post',v.novo_post, name='novo_post'),
]