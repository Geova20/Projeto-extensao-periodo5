from django.urls import path
from . import views


urlpatterns = [
    path('', views.responder_pesquisa, name='responder_pesquisa'),
    path('resultados/', views.resultados, name='resultados'),
]