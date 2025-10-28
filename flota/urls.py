from django.urls import path
from . import views


urlpatterns = [
  path('registrar', views.Registrar,name='registrar'),
  path('r_combustible/<int:ambulancia_id>', views.R_combustible,name='r_combustible'),
  path("cargar_c/<int:ambulancia_id>", views.Cargar_c, name="cargar_c"),
  path("informacion/<int:ambulancia_id>", views.Infamb, name="informacion"),
  path("historial_tanqueo/<int:ambulancia_id>", views.Tanqueo, name="historial_tanqueo"),
  path("busqueda_tanqueo/<int:ambulancia_id>", views.B_tanqueo, name="busqueda_tanqueo"),
  path("Busqueda/<int:ambulancia_id>", views.Busqueda, name="Busqueda"),
  #path('informe-tanqueo/<int:ambulancia_id>/<id>',views.informetanqueoPdf.as_view(),name='informe-tanqueo'),
  #path('informe/<int:ambulancia_id>/<id>',views.render_pdf_view,name='informe'),
  path("informe_tanqueo/<int:ambulancia_id>/<int:id>",views.tanqueo_info,name="informe_tanqueo"),
  #MANTENIMIENTO R_mantenimiento     historial_mantenimiento mantenimiento_info
  path('R_mantenimiento/<int:ambulancia_id>', views.R_mantenimiento,name='R_mantenimiento'),#
  path('historial_mantenimiento/<int:ambulancia_id>', views.historial_mantenimiento,name='historial_mantenimiento'),
  path('mantenimiento_info/<int:ambulancia_id>/<int:id>', views.mantenimiento_info,name='mantenimiento_info'),

  path('R_motor/<int:ambulancia_id>', views.R_motor,name='R_motor'),#1
  path('R_sist_combustible/<int:ambulancia_id>', views.R_sist_combustible,name='R_sist_combustible'),#2
  path('R_interiores/<int:ambulancia_id>', views.R_interiores,name='R_interiores'),#3
  path('R_carroceria/<int:ambulancia_id>', views.R_carroceria,name='R_carroceria'),#4
  path('R_sist_electrico/<int:ambulancia_id>', views.R_sist_electrico,name='R_sist_electrico'),#5
  path('R_sist_frenado/<int:ambulancia_id>', views.R_sist_frenado,name='R_sist_frenado'),#6
  path('R_sist_suspension/<int:ambulancia_id>', views.R_sist_suspension,name='R_sist_suspension'),#7
  path('R_sist_transmision/<int:ambulancia_id>', views.R_sist_transmision,name='R_sist_transmision'),#8G_motor


  path('G_motor/<int:ambulancia_id>', views.G_motor,name='G_motor'),#1
  path('G_sist_combustible/<int:ambulancia_id>', views.G_sist_combustible,name='G_sist_combustible'),#2
  path('G_interiores/<int:ambulancia_id>', views.G_interiores,name='G_interiores'),#3
  path('G_carroceria/<int:ambulancia_id>', views.G_carroceria,name='G_carroceria'),#4
  path('G_sist_electrico/<int:ambulancia_id>', views.G_sist_electrico,name='G_sist_electrico'),#5
  path('G_sist_frenado/<int:ambulancia_id>', views.G_sist_frenado,name='G_sist_frenado'),#6
  path('G_sist_suspension/<int:ambulancia_id>', views.G_sist_suspension,name='G_sist_suspension'),#7
  path('G_sist_transmision/<int:ambulancia_id>', views.G_sist_transmision,name='G_sist_transmision'),#8G_motor
  
  path('form_preopreacional/<int:ambulancia_id>', views.operacinal,name='form_preopreacional'),
  path('preoperacional/<int:ambulancia_id>', views.pre,name='preoperacional'),
 
  path('actualizarusuario', views.actualizarusuario,name='actualizarusuario'),
  path('cuentausuario', views.cuentausuario,name='cuentausuario'),
  path('hist_preoperacional/<int:ambulancia_id>', views.hist_preoperacional,name='hist_preoperacional'),
  
]


 