from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Tu nombre',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Tu email',
        'class': 'form-control'
    }))
    asunto = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Asunto (opcional)',
        'class': 'form-control'
    }))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Tu mensaje',
        'class': 'form-control',
        'rows': 5
    }))