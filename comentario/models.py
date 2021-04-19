from django.db import models
from posts.models import Post
from django.utils import timezone
from django.contrib.auth.models import User


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=150, verbose_name='Nome do autor')
    email_comentario = models.EmailField(verbose_name='Email do autor')
    comentario = models.TextField(verbose_name='Comentário')
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post comentado')
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name='Usuario', null=True, blank=True)
    data_comentario = models.DateTimeField(default=timezone.now, verbose_name='Data')
    publicado_comentario = models.BooleanField(default=False, verbose_name='Publicado')


    def __str__(self):
        return self.nome_comentario