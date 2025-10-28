from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from .forms import SubirDumentoImagenForm
from .models import Registros,Ambulancia,Correctivo,preoperacional,Cliente
from django.contrib.auth.models import User
# from .models import Registros    SubirDumentoImagen
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .utils import render_to_pdf

from django.views.generic import View
from django.db.models import Sum

from datetime import datetime 


#from io import BytesIO # nos ayuda a convertir un html en pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import os 
from django.conf import settings
from django.contrib.staticfiles import finders



    
@login_required
def Registrar(request):
    lista_ambulancias=Ambulancia.objects.all()
    cliente = get_object_or_404(Cliente, usuario=request.user)
    context={
       "ambulancias":lista_ambulancias,
       "cliente":cliente
    }
   
    return render(request, 'flota/registrar.html',context)



# @login_required
# def Cargar_c(request,ambulancia_id):
#     movil = Ambulancia.objects.get(pk=ambulancia_id)
#     if request.method == "POST":
#         form = SubirDumentoImagenForm(request.POST, request.FILES)
        
         
#         if form.is_valid():
#             # Obtenemos el usuario actualmente autenticado
#             usuario_autenticado = request.user
            
#             # Creamos una instancia del modelo con los datos del formulario
#             instancia = form.save(commit=False)
            
#             # Asignamos el usuario como autor de la instancia
#             instancia.autor = usuario_autenticado
#             instancia.movil=movil
            
            
#             # Guardamos la instancia en la base de datos
#             instancia.save()
#             form.save()
#         return redirect("informacion",ambulancia_id=movil.id)
 

@login_required
def Infamb(request,ambulancia_id):
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
   
    context = {
        "ambulancia":objambulancia,
    }
    return render(request, 'flota/informacion.html',context)



# Create your views here.
class informetanqueoPdf(View):

    def get(self, request,ambulancia_id,id, *args, **kwargs):
        listaregistro = Registros.objects.get(pk=id)
        objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        print(listaregistro)
        data = {
        'registro':listaregistro,
        'ambulancia':objambulancia,
        'fecha_actual':fecha_actual,
        }
        pdf = render_to_pdf('flota/lista.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



def render_pdf_view(request,ambulancia_id,id):
    template_path = 'flota/lista.html'
    listaregistro = Registros.objects.get(pk=id)
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    print(listaregistro)
    data = {
        'registro':listaregistro,
        'ambulancia':objambulancia,
        'fecha_actual':fecha_actual,
    }   
    context = data
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path


######## tanqueo #########

"""  mostrar  form de tanqueo """
@login_required
def R_combustible(request,ambulancia_id):
    form = SubirDumentoImagenForm()
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
        'form': form
    }

   
    return render(request, 'flota/r_combustible.html',context)
@login_required
def Cargar_c(request,ambulancia_id):
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    mensaje="no hicimos nada "
    if request.method == "POST": 
        formato=SubirDumentoImagenForm(request.POST,request.FILES)

        if formato.is_valid():
           
            dataregistro =formato.cleaned_data
            nuevoregistro=Registros()
            nuevoregistro.autor=request.user
            nuevoregistro.movil=movil
            nuevoregistro.kilometraje=dataregistro["kilometraje"]
            nuevoregistro.remicion=dataregistro["remicion"]
            nuevoregistro.foto=dataregistro["foto"]
            nuevoregistro.firma=dataregistro["firma"]
            nuevoregistro.fecha_registro=dataregistro["fecha"]
            nuevoregistro.costo=dataregistro["costo"]
            nuevoregistro.galones=dataregistro["galones"]

            nuevoregistro.save()
            mensaje="si pudimos"
    context = {
        "mensaje":mensaje,
        "ambulancia":movil,
    }


    return redirect('/flota/informacion/{}'.format(ambulancia_id))
    #render(request, 'flota/informacion.html',context)


"""  mostrar el hitorial de tanqueo"""
def Tanqueo(request,ambulancia_id):
    listaregistro = Registros.objects.filter(movil_id=ambulancia_id)
    # Sumar todos los costos de los registros de tanqueo de la ambulancia
    total_cost = listaregistro.aggregate(Sum('costo'))['costo__sum']
    print(total_cost)
    # Manejar el caso donde no hay registros (total_cost será None)
    if total_cost is None:
        total_cost = 0



    for registro in listaregistro:
        print(registro.costo)
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    context = {
        'registros':listaregistro,
        'ambulancia':objambulancia,
        'fecha_actual':fecha_actual,
        'total':total_cost,

    }
    return render(request,'flota/historial_tanqueo.html',context)
"""  mostrar  la busqueda de tanqueo """
def B_tanqueo(request,ambulancia_id):
    fecha=request.POST['fecha']
    

    listaregistro = Registros.objects.filter(movil_id=ambulancia_id)
    busqueda = listaregistro.filter(fecha_registro=fecha)
    
    
    
    
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    
    context = {
        'registros':busqueda,
        'ambulancia':objambulancia,
    }
    return render(request,'flota/historial_tanqueo.html',context)



def Busqueda(request,ambulancia_id):
    fecha_1=request.POST['fecha_1']
    fecha_2=request.POST['fecha_2']


    # startdate = date.today()
    # enddate = startdate + timedelta(days=6)
    

    listaregistro = Registros.objects.filter(fecha_registro__range=[fecha_1, fecha_2])
                                                             

    busqueda = listaregistro.filter(movil_id=ambulancia_id)
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    
    context = {
        'registros':busqueda,
        'ambulancia':objambulancia,
    }
    return render(request,'flota/historial_tanqueo.html',context)



"""  mostrar  la informacion del registro del tanqueo  """
def tanqueo_info(request,ambulancia_id,id):
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    objregistro = Registros.objects.get(pk=id)
    context = {
        "ambulancia":objambulancia,
        "registro":objregistro
    }
    return render(request, 'flota/comprobante_tanqueo.html',context)


######## mantenimiento  #########

"""  mostrar  form de tanqueo """
@login_required
def R_mantenimiento(request,ambulancia_id):
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/R_MANTENIMIENTO.html',context)

def historial_mantenimiento(request,ambulancia_id):
    listaregistro = Correctivo.objects.filter(movil_id=ambulancia_id)
    
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    context = {
        'registros':listaregistro,
        'ambulancia':objambulancia,
        'fecha_actual':fecha_actual,

    }
    return render(request,'flota/hist_mantenimiento.html',context)


def mantenimiento_info(request,ambulancia_id,id):
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    objregistro = Correctivo.objects.get(pk=id)
    context = {
        "ambulancia":objambulancia,
        "registro":objregistro
    }
    return render(request, 'flota/comprobante_mantenimiento.html',context)

   
@login_required #1
def R_motor(request,ambulancia_id):
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_motor.html',context)

@login_required#2
def R_sist_combustible(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_sist_combustible.html',context)
     
@login_required#3
def R_interiores(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_interiores.html',context)


@login_required#4
def R_carroceria(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_carroceria.html',context)

@login_required#5
def R_sist_electrico(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_sist_electrico.html',context)

@login_required#6
def R_sist_frenado(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_sist_frenos.html',context)

@login_required#7
def R_sist_suspension(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_sist_suspension.html',context)
 
@login_required#8
def R_sist_transmision(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_transmision.html',context)
 

"""  recoger la info  de tanqueo """


@login_required #1
def G_motor(request,ambulancia_id):
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    
    
    if request.method == "POST": 
        
        autor = request.user
        movil =movil
        
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="mantenimiento del motor"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()
       
    return redirect('/flota/informacion/{}'.format(ambulancia_id))

@login_required#2
def G_sist_combustible(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    
    
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="sistema combustion"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))
     
@login_required#3
def G_interiores(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="interiores y confort"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))


@login_required#4
def G_carroceria(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="carroceria y exterior"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))

@login_required#5
def G_sist_electrico(request,ambulancia_id):
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="sistema electrico"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))

@login_required#6
def G_sist_frenado(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="sistema de frenado"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))

@login_required#7
def G_sist_suspension(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="sistema de suspencion"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))

@login_required#8
def G_sist_transmision(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        mantenimiento_sistema="trasmicion"
        clase_sistema=request.POST['motor']
        detalle_mantenimiento=request.POST['Parte del Motor:']
        repuesto=request.POST['detalle']
        lugar=request.POST['lugar']
        costo=request.POST['costo']
        kilometraje =request.POST['kilometraje']
        numero_factura=request.POST['numero_factura']
        foto_factura=request.FILES['foto_factura']
        
        nuevoregistro=Correctivo()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.mantenimiento_sistema=mantenimiento_sistema
        nuevoregistro.clase_sistema=clase_sistema
        nuevoregistro.detalle_mantenimiento=detalle_mantenimiento
        nuevoregistro.repuesto=repuesto
        nuevoregistro.lugar=lugar
        nuevoregistro.costo=costo
        nuevoregistro.kilometraje =kilometraje
        nuevoregistro.numero_factura =numero_factura
        nuevoregistro.foto_factura =foto_factura
        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))



@login_required#8

def pre(request,ambulancia_id): 
    movil = Ambulancia.objects.get(pk=ambulancia_id)
    if request.method == "POST": 
        
        autor = request.user
        movil =movil  
        fecha_registro=request.POST['fecha']
        

        #estado de presentacion 
        aseo_interno=request.POST['aseo_interno']
        aseo_externo=request.POST['aseo_externo']
        latas=request.POST['latas']
        pinturas=request.POST['pintura']
        #estado de comodidad
        silleteria=request.POST['silleteria']
        encendedor=request.POST['encendedor']
        luces_interiores=request.POST['luces_interiores']
        tapetes=request.POST['tapetes']
    
        #niveles de liquido
        n_aceitemotor=request.POST['aceite_motor']
        n_liquitofrenos=request.POST['liquido_frenos']
        n_aguradiador=request.POST['agua_radiador']
        n_aguabateria=request.POST['agua_bateria']
        n_aceitehidraulico=request.POST['aceite_hidraulico']

    
    

        #estado de presentacion
        f_combustible=request.POST['fuga']
        f_agua=request.POST['fugas_agua']
        f_aceitetrasmicion=request.POST['fugas_aceite']
        f_aceitecaja=request.POST['aceite_caja']
        f_liquidofreno=request.POST['fuga_liquido']

        #tablero de control
        instrumentos=request.POST['instrumentos']
        luces_tablero=request.POST['luces_tablero']
        nivel_combustible=request.POST['nivel_combustible']
        pito=request.POST['pito']
        odometro=request.POST['odometro']
        velocimetro=request.POST['velocimetro']
        indicador_aceite=request.POST['indicador_aceite']
        i_termperatura=request.POST['indicador_temperatura']
        sirena=request.POST['Sirena']
        

        #seguridad pasiva
        c_seguridad=request.POST['c_seguridad']
        airbags=request.POST['airbags']
        chasisycarroseria=request.POST['chasis_carroceria']
        cristales=request.POST['cristales']
        apoyacabezas=request.POST['apoyacabezas']
        estado_espejos=request.POST['estado_espejos']
        espejo_laterl=request.POST['espejos_lateral']
        espejo_izquierdo=request.POST['espejo_izquierdo']
        espejo_retrovisor=request.POST['espejo_retrovisor']
        farolas=request.POST['farolas']
        manijas_exterior=request.POST['manijas_exterior']
        parachoquesdelantero=request.POST['parachoques_delantero']
        parachoquestrasero=request.POST['parachoques_trasero']
        
        #seguridad activa
        direccion=request.POST['direccion']
        suspenciondelantera=request.POST['suspension_delantera']
        amortiguadordelantero=request.POST['amortiguadores_delantero']
        suspenciontrasera=request.POST['suspension_trasera']
        amortiguadortrasero=request.POST['amortiguadores_trasero']
        lavaparabrisa=request.POST['Lava_parabrisas']
        vidriofrontal=request.POST['vidrio_frontal']
        limpiabrisas_izquierdo=request.POST['limpiabrisas_izquierdo']
        limpiabrisas_derecho=request.POST['limpiabrisas_derecho']
        aseo_motor=request.POST['aseo_motor']
        bornes_bateria=request.POST['bornes_bateria']
        ventilador=request.POST['ventilador']
        
        #estado de luces
        altas=request.POST['altas']
        medias=request.POST['medias']
        bajas=request.POST['bajas']
        d_i_delantero=request.POST['d_i_delantero']
        d_d_delantero=request.POST['d_d_delantero']
        d_i_trasero=request.POST['d_i_trasero']
        d_d_trasero=request.POST['d_d_trasero']
        parqueo=request.POST['parqueo']
        l_freno=request.POST['l_freno']
        l_reversa=request.POST['l_reversa']
        l_placa=request.POST['l_placa']
        exploradora=request.POST['exploradoras']
        l_baliza=request.POST['l_baliza']


    #estado de llantas
        ll_i_delantero=request.POST['ll_i_delantero']
        ll_d_delantero=request.POST['ll_d_delantero']
        ll_i_trasero=request.POST['ll_i_trasero']
        ll_d_trasero=request.POST['ll_d_trasero']
        repuesto=request.POST['repuesto']
        presion=request.POST['presion_llanta']
        rines=request.POST['rines']

    #frenos

        frenos_d=request.POST['e_frenos']
        frefos_mano=request.POST['freno_mano']

    #equipi de  carretera
        gato=request.POST['gato']
        chaleco=request.POST['chaleco']
        tacos=request.POST['tacos']
        plasticos=request.POST['conos']
        guantes=request.POST['guantes']
        cruceta=request.POST['cruceta']
        Cable=request.POST['cable']
        extintor=request.POST['extintores']
        linterna=request.POST['linterna']
        linterna_con_adaptador=request.POST['encendedor']
        caja=request.POST['fusibles']
        bombillos=request.POST['bombillo']
        cuerda=request.POST['cuerda']
        kit=request.POST['inmovilizadores']

    #herramientas
        Alicate=request.POST['alicate']
        Destornillador=request.POST['destornillador']
        llave=request.POST['llave']
        juego_de_llaves=request.POST['juego_llaves']
        martillo=request.POST['martillo']
        patecabra=request.POST['patecabra']

    #dotacion 
        cilindro=request.POST['cilindro']
        cilindro_portal=request.POST['cilindro_portal']
        Camilla=request.POST['camilla']
        Camilla_Tipo=request.POST['camilla_tipo']
        Camilla_2=request.POST['camilla_2']

        tabla=request.POST['tabla']
        silla=request.POST['silla']
    
        balas=request.POST['balas']
        tabla_rigida=request.POST['tabla_rigida']
        
    #covid  
        covid=request.POST['limpieza']

    #otros 
        instalacion=request.POST['instalacion']
        clutch=request.POST['clutch']
        Exosto=request.POST['exosto']
        alarma=request.POST['alarma']
        tapa=request.POST['tapa']
        salto=request.POST['salto']
        cambios=request.POST['cambios']
    
        guaya=request.POST['guaya']
        embriage=request.POST['embrague']
        encendido=request.POST['encendido']
        tanque=request.POST['tanque']
        observaciones=request.POST['observaciones']
        
        nuevoregistro=preoperacional()
        nuevoregistro.autor = autor
        nuevoregistro.movil =movil
        nuevoregistro.fecha_registro=fecha_registro
        nuevoregistro.aseo_interno=aseo_interno
        nuevoregistro.aseo_externo=aseo_externo
        nuevoregistro. latas= latas
        nuevoregistro.pinturas=pinturas
        nuevoregistro.silleteria=silleteria
        nuevoregistro.encendedor=encendedor
        nuevoregistro.luces_interiores=luces_interiores
        nuevoregistro.tapetes=tapetes
        nuevoregistro.n_aceitemotor=n_aceitemotor
        nuevoregistro.n_liquitofrenos=n_liquitofrenos
        nuevoregistro.n_aguradiador=n_aguradiador
        nuevoregistro.n_aguabateria=n_aguabateria
        nuevoregistro.n_aceitehidraulico=n_aceitehidraulico
        nuevoregistro.f_combustible=f_combustible
        nuevoregistro.f_agua=f_agua
        nuevoregistro.f_aceitetrasmicion=f_aceitetrasmicion
        nuevoregistro.f_aceitecaja=f_aceitecaja
        nuevoregistro.f_liquidofreno=f_liquidofreno
        nuevoregistro.instrumentos=instrumentos
        nuevoregistro.luces_tablero=luces_tablero
        nuevoregistro.nivel_combustible=nivel_combustible
        nuevoregistro. pito= pito
        nuevoregistro.odometro=odometro
        nuevoregistro.velocimetro=velocimetro
        nuevoregistro.indicador_aceite=indicador_aceite
        nuevoregistro.i_termperatura=i_termperatura
        nuevoregistro.sirena=sirena
        nuevoregistro.c_seguridad=c_seguridad
        nuevoregistro.airbags=airbags
        nuevoregistro.chasisycarroseria=chasisycarroseria
        nuevoregistro.cristales=cristales
        nuevoregistro.apoyacabezas=apoyacabezas
        nuevoregistro.estado_espejos=estado_espejos
        nuevoregistro.espejo_laterl=espejo_laterl
        nuevoregistro.espejo_izquierdo=espejo_izquierdo
        nuevoregistro.espejo_retrovisor=espejo_retrovisor
        nuevoregistro.farolas=farolas
        nuevoregistro.manijas_exterior=manijas_exterior
        nuevoregistro.parachoquesdelantero=parachoquesdelantero
        nuevoregistro.parachoquestrasero=parachoquestrasero
        nuevoregistro.direccion=direccion
        nuevoregistro.suspenciondelantera=suspenciondelantera
        nuevoregistro.amortiguadordelantero=amortiguadordelantero
        
        nuevoregistro.suspenciontrasera=suspenciontrasera
        nuevoregistro.amortiguadortrasero=amortiguadortrasero
        nuevoregistro.lavaparabrisa=lavaparabrisa
        nuevoregistro.vidriofrontal=vidriofrontal
        nuevoregistro.limpiabrisas_izquierdo=limpiabrisas_izquierdo
        nuevoregistro.limpiabrisas_derecho=limpiabrisas_derecho
        nuevoregistro.aseo_motor=aseo_motor
        nuevoregistro.bornes_bateria=bornes_bateria
        nuevoregistro.ventilador=ventilador
        #estado de luces
        nuevoregistro.altas=altas
        nuevoregistro.medias=medias
        nuevoregistro.bajas=bajas
        nuevoregistro.d_i_delantero=d_i_delantero
        nuevoregistro.d_d_delantero=d_d_delantero
        nuevoregistro.d_i_trasero=d_i_trasero
        nuevoregistro.d_d_trasero=d_d_trasero
        nuevoregistro.parqueo=parqueo
        nuevoregistro.l_freno=l_freno
        nuevoregistro.l_reversa=l_reversa
        nuevoregistro.l_placa=l_placa
        nuevoregistro.exploradora=exploradora
        nuevoregistro.l_baliza=l_baliza

    #estado de llantas
        nuevoregistro.ll_i_delantero=ll_i_delantero
        nuevoregistro.ll_d_delantero=ll_d_delantero
        nuevoregistro.ll_i_trasero=ll_i_trasero
        nuevoregistro.ll_d_trasero=ll_d_trasero
        nuevoregistro.repuesto=repuesto
        nuevoregistro.presion=presion
        nuevoregistro.rines=rines

    #frenos

        nuevoregistro.frenos_d=frenos_d
        nuevoregistro.frefos_mano=frefos_mano
    #equipi de  carretera
        nuevoregistro.gato=gato
        nuevoregistro.chaleco=chaleco
        nuevoregistro.tacos=tacos
        nuevoregistro.plasticos=plasticos
        nuevoregistro.guantes=guantes
        nuevoregistro.cruceta=cruceta
        nuevoregistro.Cable=Cable
        nuevoregistro.extintor=extintor
        nuevoregistro.linterna=linterna
        nuevoregistro.linterna_con_adaptador=linterna_con_adaptador
        nuevoregistro.bombillos=bombillos
        nuevoregistro.cuerda=cuerda
        nuevoregistro.kit=kit

    #herramientas
        nuevoregistro.Alicate=Alicate
        nuevoregistro.Destornillador=Destornillador
        nuevoregistro.llave=llave
        nuevoregistro.juego_de_llaves=juego_de_llaves
        nuevoregistro.martillo=martillo
        nuevoregistro.patecabra=patecabra
    #dotacion 
        nuevoregistro.cilindro=cilindro
        nuevoregistro.cilindro_portal=cilindro_portal
        nuevoregistro.Camilla=Camilla
        nuevoregistro.Camilla_Tipo=Camilla_Tipo
        nuevoregistro.Camilla_2=Camilla_2

        nuevoregistro.tabla=tabla
        nuevoregistro.silla=silla
    
        nuevoregistro.balas=balas
        nuevoregistro.tabla_rigida=tabla_rigida
        
    #covid  
        nuevoregistro.covid=covid

    #otros 
        nuevoregistro.instalacion=instalacion
        nuevoregistro.clutch=clutch
        nuevoregistro.Exosto=Exosto
        nuevoregistro.alarma=alarma
        nuevoregistro.tapa=tapa
        nuevoregistro.salto=salto
        nuevoregistro.cambios=cambios
    
        nuevoregistro.guaya=guaya
        nuevoregistro.embriage=embriage
        nuevoregistro.encendido=encendido
        nuevoregistro.tanque=tanque
        nuevoregistro.observaciones=observaciones








        nuevoregistro.save()

    return redirect('/flota/informacion/{}'.format(ambulancia_id))



@login_required#8
def operacinal(request,ambulancia_id): 
    objambulancia= Ambulancia.objects.get(pk=ambulancia_id)
    context = {
        "movil":objambulancia,
    }  
    return render(request, 'flota/registro_preoperacional.html',context)






def actualizarusuario(request):
    
    if request.method == "POST": 
        #actualizar usuario 
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name=request.POST["nombre"]
        actUsuario.last_name=request.POST["apellido"]
        actUsuario.email=request.POST["email"]
        actUsuario.save()
        #registrar cliente 



        try:
            cliente = Cliente.objects.get(usuario=actUsuario)
        except Cliente.DoesNotExist:
            cliente = Cliente(usuario=actUsuario)

        cliente.cedula = request.POST["cedula"]
        cliente.telefono = request.POST["telefono"]
        cliente.sexo = request.POST["sexo"]
        cliente.fecha_nacimiento = request.POST["fecha_nacimiento"]
        cliente.save() 

    return redirect('/flota/registrar')
# def cuentausuario(request):
#     frmCliente=Clienteform()
#     context={
#         'form':frmCliente
#     }
#     return render(request,"cuenta.html",context)

@login_required
def cuentausuario(request): 
    
    return render(request, 'flota/perfil.html')


@login_required
def hist_preoperacional(request,ambulancia_id): 
    listaregistro = preoperacional.objects.filter(movil_id=ambulancia_id)
    
    objambulancia = Ambulancia.objects.get(pk=ambulancia_id)
    
    context = {
        'registros':listaregistro,
        'ambulancia':objambulancia,
    }
    
    return render(request,'flota/hist_preoperacional.html',context)
    
   