from django.db import models
from django.contrib.auth.models import User 
from datetime import date
from django.utils import timezone
# Create your models here.

from cloudinary.models import CloudinaryField

class  Ambulancia(models.Model):
    movil =models.CharField(max_length=100)
    clasevehiculo=models.CharField(max_length=100)
    marca=models.CharField(max_length=100)
    modelo=models.IntegerField(null=False, blank=False)
    placa=models.CharField(max_length=10)
    ven_soat=models.DateField(default=timezone.now)
    ven_tecno=models.DateField(default=timezone.now)
    frontal = CloudinaryField('imagen')
    lateral = CloudinaryField('imagen')


    def __str__(self):
        return self.movil



class  Registros(models.Model):
    autor = models.ForeignKey(User,on_delete=models.RESTRICT)
   
    fecha_registro=models.DateField(default=timezone.now)
  
    hora_registro = models.DateTimeField(default=timezone.now)
    movil = models.ForeignKey(Ambulancia,on_delete=models.RESTRICT)
    kilometraje = models.IntegerField(null=False, blank=False)
    remicion= models.IntegerField(null=False, blank=False)
    firma =CloudinaryField('imagen')
    foto = CloudinaryField('imagen')
    costo=models.DecimalField(max_digits=10,decimal_places=2,default=0)
   # galones=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    def get_last_name(self):
        return self.autor.last_name

    def __str__(self):
        return self.autor.last_name
    



class  Correctivo(models.Model):
    autor = models.ForeignKey(User,on_delete=models.RESTRICT)
    movil = models.ForeignKey(Ambulancia,on_delete=models.RESTRICT)
    hora_registro = models.DateTimeField(default=timezone.now)
    fecha_registro=models.DateField(default=timezone.now)
    mantenimiento_sistema=models.TextField()
    clase_sistema=models.TextField()
    detalle_mantenimiento=models.TextField()
    repuesto=models.CharField(max_length=30)
    lugar=models.TextField()
    costo=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    kilometraje = models.IntegerField(null=False, blank=False)
    numero_factura= models.IntegerField(null=False, blank=False)
    foto_factura= CloudinaryField('imagen')
   
    
    def __str__(self):
        return self.movil
    

class preoperacional(models.Model):
    autor = models.ForeignKey(User,on_delete=models.RESTRICT)
    movil = models.ForeignKey(Ambulancia,on_delete=models.RESTRICT)
    hora_registro = models.DateTimeField(default=timezone.now)
    fecha_registro=models.DateField(default=timezone.now)

    #estado de presentacion 
    aseo_interno=models.TextField()
    aseo_externo=models.TextField()
    latas=models.TextField()
    pinturas=models.TextField()

    #estado de comodidad
    silleteria=models.TextField()
    encendedor=models.TextField()
    luces_interiores=models.TextField()
    tapetes=models.TextField()
   
    #niveles de liquido
    n_aceitemotor=models.TextField()
    n_liquitofrenos=models.TextField()
    n_aguradiador=models.TextField()
    n_aguabateria=models.TextField()
    n_aceitehidraulico=models.TextField()

   
   

    #estado de presentacion
    f_combustible=models.TextField()
    f_agua=models.TextField()
    f_aceitetrasmicion=models.TextField()
    f_aceitecaja=models.TextField()
    f_liquidofreno=models.TextField()

    #tablero de control
    instrumentos=models.TextField()
    luces_tablero=models.TextField()
    nivel_combustible=models.TextField()
    pito=models.TextField()
    odometro=models.TextField()
    velocimetro=models.TextField()
    indicador_aceite=models.TextField()
    i_termperatura=models.TextField()
    sirena=models.TextField()
    

    #seguridad pasiva
    c_seguridad=models.TextField()
    airbags=models.TextField()
    chasisycarroseria=models.TextField()
    cristales=models.TextField()
    apoyacabezas=models.TextField()
    estado_espejos=models.TextField()
    espejo_laterl=models.TextField()
    espejo_izquierdo=models.TextField()
    espejo_retrovisor=models.TextField()
    farolas=models.TextField()
    manijas_exterior=models.TextField()
    parachoquesdelantero=models.TextField()
    parachoquestrasero=models.TextField()
    
    #seguridad activa
    direccion=models.TextField()
    suspenciondelantera=models.TextField()
    amortiguadordelantero=models.TextField()
    suspenciontrasera=models.TextField()
    amortiguadortrasero=models.TextField()
    lavaparabrisa=models.TextField()
    vidriofrontal=models.TextField()
    limpiabrisas_izquierdo=models.TextField()
    limpiabrisas_derecho=models.TextField()
    aseo_motor=models.TextField()
    bornes_bateria=models.TextField()
    ventilador=models.TextField()
    
    #estado de luces
    altas=models.TextField()
    medias=models.TextField()
    bajas=models.TextField()
    d_i_delantero=models.TextField()
    d_d_delantero=models.TextField()
    d_i_trasero=models.TextField()
    d_d_trasero=models.TextField()
    parqueo=models.TextField()
    l_freno=models.TextField()
    l_reversa=models.TextField()
    l_placa=models.TextField()
    exploradora=models.TextField()
    l_baliza=models.TextField()


  #estado de llantas
    ll_i_delantero=models.TextField()
    ll_d_delantero=models.TextField()
    ll_i_trasero=models.TextField()
    ll_d_trasero=models.TextField()
    repuesto=models.TextField()
    presion=models.TextField()
    rines=models.TextField()
    

 #frenos

    frenos_d=models.TextField()
    frefos_mano=models.TextField()

#equipi de  carretera
    gato=models.TextField()
    chaleco=models.TextField()
    tacos=models.TextField()
    plasticos=models.TextField()
    guantes=models.TextField()
    cruceta=models.TextField()
    Cable=models.TextField()
    extintor=models.TextField()
    linterna=models.TextField()
    linterna_con_adaptador=models.TextField()
    caja=models.TextField()
    bombillos=models.TextField()
    cuerda=models.TextField() 
    kit=models.TextField()

#herramientas
    Alicate=models.TextField()
    Destornillador=models.TextField()
    llave=models.TextField()
    juego_de_llaves=models.TextField()
    martillo=models.TextField()
    patecabra=models.TextField()

#dotacion 
    cilindro=models.TextField()
    cilindro_portal=models.TextField()
    Camilla=models.TextField()
    Camilla_Tipo=models.TextField()
    Camilla_2=models.TextField()

    tabla=models.TextField()
    silla=models.TextField()
   
    balas=models.TextField()
    tabla_rigida=models.TextField()
     
#covid  
    covid=models.TextField()

#otros 
    instalacion=models.TextField()
    clutch=models.TextField()
    Exosto=models.TextField()
    alarma=models.TextField()
    tapa=models.TextField()
    salto=models.TextField()
    cambios=models.TextField()
   
    guaya=models.TextField()
    embriage=models.TextField()
    encendido=models.TextField()
    tanque=models.TextField()
    observaciones=models.TextField()
    
    def __str__(self):
        return self.movil
    
class Cliente(models.Model):
    usuario= models.OneToOneField(User,on_delete=models.RESTRICT)
    cedula=models.CharField(max_length=10)
    sexo=models.CharField(max_length=10,default="M")
    telefono=models.CharField(max_length=20)
    fecha_nacimiento=models.DateField(null=True)

    def __str__(self):
        return self.cedula