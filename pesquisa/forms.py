from django import forms
from .models import Pessoa, Finalidade


class PessoaForm(forms.ModelForm):

    nome = forms.CharField(
        error_messages={
            'required': 'É necessário preencher este campo para enviar a resposta.'
        }
    )

    email = forms.EmailField(
        error_messages={
            'required': 'É necessário preencher este campo para enviar a resposta.',
            'invalid': 'Informe um endereço de e-mail válido.'
        }
    )

    FAIXAS_ETARIAS = [
        ('ate-18', 'Até 18 anos'),
        ('19-30', '19 a 30 anos'),
        ('31-50', '31 a 50 anos'),
        ('51+', '51 anos ou mais'),
    ]

    faixa_etaria = forms.ChoiceField(
        choices=FAIXAS_ETARIAS,
        widget=forms.RadioSelect,
        label='Faixa etária',
        error_messages={
            'required': 'É necessário selecionar sua faixa etária para enviar a resposta.'
        }
    )

    finalidades = forms.ModelMultipleChoiceField(
        queryset=Finalidade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Quais são as principais finalidades para as quais você mais utiliza a tecnologia?',
        help_text='Selecione de 1 a 3 opções.',
        required=True,
        error_messages={
            'required': 'Selecione pelo menos uma finalidade.'
        }
    )

    class Meta:
        model = Pessoa
        fields = ['nome', 'email', 'faixa_etaria']

    def clean_email(self):
        email = self.cleaned_data['email']

        if Pessoa.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este e-mail já foi utilizado para responder à pesquisa.'
            )

        return email

    def clean_finalidades(self):
        finalidades = self.cleaned_data['finalidades']

        if len(finalidades) > 3:
            raise forms.ValidationError(
                'Selecione no máximo 3 finalidades.'
            )

        return finalidades