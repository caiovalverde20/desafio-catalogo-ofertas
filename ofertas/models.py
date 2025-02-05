from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.URLField()
    link = models.URLField()
    parcelamento = models.CharField(max_length=100, blank=True, null=True)
    preco_sem_desconto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tipo_entrega = models.CharField(max_length=50, choices=[("full", "Full"), ("normal", "Normal")], blank=True, null=True)
    frete_gratis = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
