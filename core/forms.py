from django import forms
from .models import MicroLeccion, Tarea, SesionEstudio



class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'minutos_estimados', 'completada']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'minutos_estimados': forms.NumberInput(attrs={'class': 'form-control'}),
            'completada': forms.CheckboxInput(attrs={'class': ''}),
        }



class SesionEstudioForm(forms.ModelForm):
    class Meta:
        model = SesionEstudio
        fields = ['tarea', 'tipo_sesion', 'duracion_minutos', 'inicio_en', 'notas']
        widgets = {
            'inicio_en': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MicroLeccionForm(forms.ModelForm):
    class Meta:
        model = MicroLeccion
        fields = ['titulo', 'contenido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
