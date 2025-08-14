from django.db import models

# Create your models here.
class Post(models.Model):
    nome = models.CharField(max_length=50)
    imagem = models.ImageField(blank=True,null=True)
    cor = models.CharField(max_length=20)
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False) 
