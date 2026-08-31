from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    faixa_etaria = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Finalidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class PessoaFinalidade(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    finalidade = models.ForeignKey(Finalidade, on_delete=models.CASCADE)
    outro_descricao = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pessoa', 'finalidade'],
                name='pessoa_finalidade_unica'
            )
        ]