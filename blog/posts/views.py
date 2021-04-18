from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentario.forms import FormComentario
from comentario.models import Comentario
from posts.forms import FormPost


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'
    get_object_or_404 = get_object_or_404

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios = Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria',None)
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'
    get_object_or_404 = get_object_or_404

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario=True, post_comentario=post.id)
        contexto['comentarios'] = comentarios
        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user
        comentario.save()

        return redirect('post_detalhes',pk=post.id)


def sobre(request):
    
    return render(request,'posts/sobre.html')


def novo_post(request):
    if request.method == 'POST':
        form_post = FormPost(request.POST)
        if form_post.is_valid():
            form_post.save()
            return redirect('novo_post')
    else:
        form_post = FormPost()
        post = {'post': form_post}
        return render(request, 'posts/novo_post.html', context=post)
    return redirect('novo_post')