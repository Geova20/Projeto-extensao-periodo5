from django.contrib import admin

from .models import Pessoa, Finalidade, PessoaFinalidade

admin.site.register(Pessoa)
admin.site.register(Finalidade)
admin.site.register(PessoaFinalidade)
