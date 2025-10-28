from django import forms
from django.core.validators import FileExtensionValidator



class DateInput(forms.DateInput):
    input_type="date"

class SubirDumentoImagenForm(forms.Form):
    
    fecha=forms.DateField(label="Fecha",input_formats=["%Y-%m-%d"],widget=DateInput(),required=True)
    kilometraje=forms.IntegerField(label="kilometraje",required=True)
    remicion=forms.CharField(label="numero de remicion" , max_length=10,required=True)
    costo=forms.DecimalField(label="Costo del combustible",max_digits=10,decimal_places=2,required=True)
    galones=forms.DecimalField(label="galones:",max_digits=10,decimal_places=2,required=True)
    firma=forms.FileField(label="foto de remicion" ,required=True, help_text='Por favor, carga una imagen', 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    foto=forms.FileField(label="foto del kilometraje" ,required=True, help_text='Por favor, carga una imagen', 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
 
    
 




   
