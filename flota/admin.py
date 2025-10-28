from django.contrib import admin



from .models import Registros,Ambulancia



@admin.register(Ambulancia)
class AmbulnciaAdmin(admin.ModelAdmin):
    list_display=('movil','placa','ven_soat','ven_tecno',)
    list_editable=('ven_soat','ven_tecno',)





admin.site.register(Registros)

 
