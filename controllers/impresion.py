# -*- coding: utf-8 -*-
# try something like

from subprocess import Popen, PIPE
import os
import uuid
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm, inch, cm
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, Table, Spacer
from reportlab.platypus import SimpleDocTemplate, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import datetime

#c.showPage()
#c.save()

def def_pags_datos(idpedido):
    '''Extraer los detalles del pedido'''
    detalle_pedido=db(db.tbl_itempedido.idpedido==idpedido).select(db.tbl_itempedido.referencia,
                                                                   db.tbl_itempedido.decripcion,
                                                                   db.tbl_itempedido.um,
                                                                   db.tbl_itempedido.bodega,
                                                                   db.tbl_itempedido.cantped,
                                                                   db.tbl_itempedido.catcomp,
                                                                   db.tbl_itempedido.catpte,
                                                                   db.tbl_itempedido.precio,
                                                                   db.tbl_itempedido.total,
                                                                   db.tbl_itempedido.iva,
                                                                   orderby=db.tbl_itempedido.bodega)# |db.tbl_itempedido.id)#,limitby=(0,38))
    if detalle_pedido ==None:
        return None

    salida=[]
    for item in detalle_pedido:
        salida.append((item.referencia,item.decripcion,item.um,item.bodega,item.cantped,item.catcomp,item.catpte,' ',item.precio,item.total,item.iva))
    return salida

def tabla_detalle(detalle_pedido):
    tempdatos=[
            ("Referencia","Decripción","Und","Bod.","Cant.\nPedida","Cant.\nCompr.","Cant.\nPend.","Separ.","Vlr.\nUnitario","Total","Iva"),
           ]
    for items in detalle_pedido:
        tempdatos.append(items)
    
    tabla = Table(tempdatos,colWidths=(16*mm, 69*mm , 9*mm, 7*mm, 12*mm, 12*mm, 12*mm, 14*mm, 21*mm, 22*mm, 8*mm)) #None,4 * mm)
    tabla.setStyle (TableStyle ([('FONTSIZE', (0, 0), (-1, -1), 7.5),
                                 ('TEXTFONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                 ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#D2D6CC')),
                                 ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                                 ('ALIGNMENT', (4, 1), (-1, -1), 'RIGHT'),
                                 ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D2D6CC')),# colors.blue),
                                 ('BOX', (0, 0), (-1, -1), 1, colors.green),
                                 ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                 ('BOTTOMPADDING',(0,0),(-1,-1),1),
                                 ]))
    return tabla

def encabezado1pag(c,consulta_pedido,pagina=1,paginas=1):
    width, height = letter
    consultacliente = db (db.tbl_cliente.id== consulta_pedido.idcliente).select().first()
    if consulta_pedido.idenvio==None:
        consultaenvio=None
    else:
        consultaenvio=db (db.tbl_envio.id==consulta_pedido.idenvio).select().first()
    vendedor=db(db.auth_user.id==consulta_pedido.idvendedor).select (db.auth_user.first_name).first()
    c.setFont("Helvetica-Bold",11)
    #c.drawCentredString(width/2, 269.4* mm,"REDOX - PEDIDO DEL CLIENTE")
    c.drawString(7 * mm, 269.4 * mm,"REDOX - PEDIDO DEL CLIENTE")
    c.setFont("Helvetica",7)
    c.drawString(14 * mm, 252 * mm, "Separador")
    c.drawString(45 * mm, 252 * mm, "Empacador")
    #c.drawString(110 * mm, 257 * mm, "CALLE 9C NO. 23C - 51")
    #c.drawString(110 * mm, 254 * mm, "Tel: 5246000 - CALI")
    #c.drawString(110 * mm, 251 * mm, "Nit: 800078360-4")
    barcode = code128.Code128( consulta_pedido.nropedido ,barHeight=.5*inch,barWidth = 1)
    barcode.drawOn(c, 140*mm, 264*mm)
    c.setFont("Helvetica",8)
    #fecha + hora + pag
    c.drawString(15.1 * cm, 256 * mm, "Fecha CGUno")
    c.drawString(17 * cm, 256 * mm, ": " + consulta_pedido.fecha.strftime('%m/%d/%Y'))
    c.drawString(18.8 * cm, 256 * mm, consulta_pedido.hora)
    c.drawString(15.1 * cm, 253 * mm, "Fecha Sistema")
    c.drawString(17 * cm, 253 * mm, ": " + datetime.datetime.now().strftime('%m/%d/%Y   %H:%M:%S')) #consulta_pedido.fechasis.strftime('%m/%d/%Y'))
    
    c.drawString(15.1 * cm, 250 * mm, "Pagina")
    c.drawString(17 * cm, 250 * mm, ": %s/%s" %(pagina,paginas))

    #col Cliente
    c.drawString(165 * mm, 260 * mm, consulta_pedido.nropedido )
    c.drawString(8 * mm, 244 * mm, "Cliente")
    c.drawString(22 * mm, 244 * mm, ": " + consultacliente.nombre)
    c.drawString(8 * mm, 240.5 * mm, "Contacto")
    c.drawString(22 * mm, 240.5 * mm, ": " + consultacliente.contacto)
    c.drawString(8 * mm, 237.0 * mm, "Nit")
    c.drawString(22 * mm, 237 * mm, ": " + consultacliente.nit)
    c.drawString(8 * mm, 233.5 * mm, "Direccion")
    c.drawString(22 * mm, 233.5 * mm, ": " + consultacliente.direccion)
    c.drawString(8 * mm, 230.0 * mm, "Ciudad")
    c.drawString(22 * mm, 230 * mm, ": " + consultacliente.ciudad)
    c.drawString(8 * mm, 226.5 * mm, "Telefono")
    c.drawString(22 * mm, 226.5 * mm, ": " + consultacliente.telefono)
    #columna 2
    c.drawString(8 * cm, 244 * mm, "Pto. de Envio")
    c.drawString(8 * cm, 240.5 * mm, "Dir. Envio")
    c.drawString(8 * cm, 237.0 * mm, "Ciudad Envio")
    c.drawString(8 * cm, 233.5 * mm, "Contacto Pto.")
    c.drawString(8 * cm, 230.0 * mm, "Telefono Pto.")
    c.drawString(8 * cm, 226.5 * mm, "Doc. Alterno")
    if not consultaenvio==None:
        c.drawString(10.1 * cm, 244 * mm, ": " + consultaenvio.ptoenvio)
        c.drawString(10.1 * cm, 240.5 * mm, ": " + consultaenvio.direnvio)
        c.drawString(10.1 * cm, 237 * mm, ": " + consultaenvio.ciudadenvio)
        c.drawString(10.1 * cm, 233.5 * mm, ": " + consultaenvio.contactopto)
        c.drawString(10.1 * cm, 230 * mm, ": " + consultaenvio.telpto)
        c.drawString(10.1 * cm, 226.5 * mm, ": " + consultaenvio.dcoalterno)
    #columna3
    c.drawString(15 * cm, 244 * mm, "Vendedor")
    c.drawString(16.9 * cm, 244 * mm, ": " + vendedor.first_name.title())
    c.drawString(15 * cm, 240.5 * mm, "O..Compra #")
    if consulta_pedido.ordencompra:
        c.drawString(16.9 * cm, 240.5 * mm, ": " +  consulta_pedido.ordencompra)
    c.drawString(15 * cm, 237.0 * mm, "Cond.de Pago")
    if consulta_pedido.condpago:
        c.drawString(16.9 * cm, 237 * mm, ": " + consulta_pedido.condpago)
    c.drawString(15 * cm, 233.5 * mm, "Zona")
    if consulta_pedido.zona:
        nombrezona=db(db.tbl_zonaventas.id==consulta_pedido.zona).select(db.tbl_zonaventas.nombre).first()
        c.drawString(16.9 * cm, 233.5 * mm, ": " + nombrezona.nombre)
    c.drawString(15 * cm, 230.0 * mm, "Fecha Entrega")
    temp=consulta_pedido.fentrega.strftime('%m/%d/%Y')
    c.drawString(16.9 * cm, 230 * mm, ": " + consulta_pedido.fentrega.strftime('%m/%d/%Y'))
    c.drawString(15 * cm, 226.5 * mm, "Elaborado por:")
    c.drawString(16.9 * cm, 226.5 * mm, ": " + consulta_pedido.elaborado)
    #c.setStrokeColor(colors.red)

    #Encabezado
    c.setStrokeColor(colors.green)
    c.roundRect(x=7 * mm, y=25 * cm , width= 6 * cm , height=1.8 * cm, radius=10, stroke=1, fill=0)
    c.roundRect(x=70 * mm, y=25 * cm , width= 7 * cm , height=2.4 * cm, radius=10, stroke=1, fill=0)
    c.roundRect(x=7 * mm, y=22.5 * cm , width= width - (15*mm), height=2.3 * cm, radius=10, stroke=1, fill=0)
    c.setLineWidth(.5)
    #lineas par separaqcion
    c.line(8 *mm , 25.5 * cm , 3.3 * cm,  25.5 * cm)
    c.line(3.8 *cm , 25.5 * cm , 6.3 * cm,  25.5 * cm)

    #col2
    c.line(7.9 * cm, 22.5 * cm , 7.9 * cm,  24.8 * cm)
    #col3
    c.line(14.9 * cm, 22.5 * cm , 14.9 * cm,  24.8 * cm)
    #pie
    ##c.roundRect(x=6 * mm, y=15.5 * cm  , width= width - (12*mm), height=1 * cm, radius=10, stroke=1, fill=0)

def pie(consulta_pedido):
    campos = [('Total Bruto','Dto.X Linea','Dto.Global 0%','Sub Total','Valor Iva','T O T A L','Nro. Cajas','Nro Paquetes'),
              ("$ {0:2,.2f}".format(consulta_pedido.totalbruto), "$ {0:2,.2f}".format(consulta_pedido.dscoxlinea) ,
               "$ {0:2,.2f}".format(consulta_pedido.dsctglobal), "$ {0:2,.2f}".format(consulta_pedido.subtotal) ,
               "$ {0:2,.2f}".format(consulta_pedido.valoriva) ,  "$ {0:2,.2f}".format(consulta_pedido.total),
               "",""
              )
             ]
    ##mod abril 2017  
    ##tabla = Table(campos,colWidths=(30*mm, 30*mm , 27*mm, 30*mm, 30*mm, 25*mm, 32*mm))
    tabla = Table(campos,colWidths=(29*mm, 24*mm , 24*mm, 30*mm, 24*mm, 31*mm, 2 *cm, 2 *cm))
    tabla.setStyle (TableStyle ([('FONTSIZE', (0, 0), (-1, -1), 8),
                                 ('TEXTFONT', (0, 0), (-1, -1), 'Arial-Bold'),
                                 ('ALIGNMENT', (0,0), (-1, -1), 'CENTER'),
                                 ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D2D6CC')),
                                 ('BOX', (0, 0), (-1, -1), 1, colors.green),
                                ]))
    return tabla

def encabezado2pag(c,consulta_pedido,pagina=1,paginas=1):
    #Encabezado de anexos
    width, height = letter
    consultacliente = db (db.tbl_cliente.id== consulta_pedido.idcliente).select().first()
    c.setFont("Helvetica-Bold",12)
    c.drawCentredString(width/2, 269.4* mm,"PEDIDO DEL CLIENTE")
    c.setFont("Helvetica",7)
    c.drawString(17 * cm, 271 * mm, "Nro Pedido:" + consulta_pedido.nropedido )
    c.drawString(17 * cm, 268 * mm, "Fecha:" + datetime.datetime.now().strftime('%m/%d/%Y    %H:%M:%S'))
    c.drawString(17 * cm, 265 * mm, "Pagina: %s/%s" %(pagina,paginas))
    c.setStrokeColor(colors.green)
    c.roundRect(x=16.8 * cm, y=10.4 * inch , width= 3.5 * cm , height=1 * cm, radius=5, stroke=1, fill=0)
    c.line(0 * cm, 10.4 * inch , 16.8 * cm ,  10.4 * inch)


def index():
    idpedido=request.args(0)#2
    posxtabla= 7 * mm
    max_mediaCarta=9
    salidamediacarta=False
    max_Carta= 31 #lineas max para genereran 1 sola pagina carta
    max_Carta1L=35 #Lineas max para carta con encabezado 1 pag
    max_Carta2L=42 #Linea max para carta con encabezado2 
    max_Carta3L=39 #pagina final con pie + encabedo ultima pag
    
    tmp_uuid = uuid.uuid4()
    ruta = os.path.join(request.folder,"temp","%s.pdf"%tmp_uuid)
    consulta_pedido=db(db.tbl_pedido.id==idpedido).select().first()

    detalle_pedido = def_pags_datos(idpedido)
    #cacular pos tabla y pie
    if detalle_pedido ==None:
	    return "error:No hay items del pedido"

    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter

    lnsdetalle=len(detalle_pedido)

    if lnsdetalle <=max_mediaCarta:#Media carta 1pag
        salidamediacarta=True
        #solo una pagina
        ##c = canvas.Canvas(ruta, pagesize=landscape(letter))
        ##width, height = letter
    

        tabla=tabla_detalle(detalle_pedido)
        tabla.wrapOn(c, width - 1*cm , height)
        posy_iniTabla = (height /2) + 2.3 * cm 
        ##posy_iniTabla =  2.3 * cm 
        if lnsdetalle <max_mediaCarta:
        	posy_iniTabla += ((max_mediaCarta - lnsdetalle) *  (5.6 * mm))
        tabla.drawOn(c, posxtabla ,  posy_iniTabla)
        pie_tabla=pie(consulta_pedido)
        pie_tabla.wrapOn(c, width - 1*cm , height)
        pie_tabla.drawOn(c, posxtabla ,  posy_iniTabla - (1.4 * cm))
        c.line(0, 5.5*inch, width, 5.5*inch)
        #Encabezado
        encabezado1pag(c,consulta_pedido)
        c.save()
        
    elif lnsdetalle <=max_Carta:#Carta 1pag
        c = canvas.Canvas(ruta, pagesize=letter)
        width, height = letter
        #solo una pagina
        tabla=tabla_detalle(detalle_pedido)
        tabla.wrapOn(c, width - 1*cm , height)
        posy_iniTabla = 26.6 * mm
        if lnsdetalle <max_Carta: #mover a una nueva posicion en y
        	posy_iniTabla += ((max_Carta - lnsdetalle) *  (5.65 * mm))
        tabla.drawOn(c, posxtabla ,  posy_iniTabla)
        pie_tabla=pie(consulta_pedido)
        pie_tabla.wrapOn(c, width - 1*cm , height)
        pie_tabla.drawOn(c, posxtabla ,  posy_iniTabla - (1.4 * cm))
        #Encabezado
        encabezado1pag(c,consulta_pedido)
        c.save()

    else:
        c = canvas.Canvas(ruta, pagesize=letter)
        width, height = letter
        #encabezado Mas de una pagina carta
        result ="lineas detalle inicial =%s   " % lnsdetalle
        lnsdetalle=lnsdetalle - max_Carta1L  #se resta la primera pagina
        if lnsdetalle <=0:
            paginas=2
        else:
            paginas = 2 + int (lnsdetalle/max_Carta2L) #Nro paginas 
        result +="calculo de paginas %s   lnd:%s" % (paginas, lnsdetalle)
        for pagina in range(1,paginas+1):
            if pagina ==1:
                encabezado1pag(c,consulta_pedido,pagina,paginas)
                parte_detalle =detalle_pedido[0:max_Carta1L]
                detalle_pedido=detalle_pedido[max_Carta1L:]
                posy_iniTabla = 5 * mm + ( max_Carta1L - len(parte_detalle)+3) * 5.65 
    
            elif pagina==paginas: #pagina final
                encabezado2pag(c,consulta_pedido,pagina,paginas)
                if len(detalle_pedido) >0:
                    tabla=tabla_detalle(detalle_pedido)
                    tabla.wrapOn(c, width - 1*cm , height)
                    posy_iniTabla = 25 * mm
                    lnsdetalle = len(detalle_pedido)
                    posy_iniTabla += ((max_Carta3L - lnsdetalle) *  (5.65 * mm))
                    tabla.drawOn(c, posxtabla ,  posy_iniTabla)
                else:
                    posy_iniTabla = 10 * inch
                pie_tabla=pie(consulta_pedido)
                pie_tabla.wrapOn(c, width - 1*cm , height)
                pie_tabla.drawOn(c, posxtabla ,  posy_iniTabla - (1.5 * cm))
                c.showPage()
                break

            else:#resto de paginas
                #cabezado2
                encabezado2pag(c,consulta_pedido,pagina,paginas)
                parte_detalle =detalle_pedido[0:max_Carta2L]
                detalle_pedido=detalle_pedido[max_Carta2L:]
            tabla=tabla_detalle(parte_detalle)
            tabla.wrapOn(c, width - 1*cm , height)
            #posy_iniTabla = 7 * mm
            tabla.drawOn(c, posxtabla ,  posy_iniTabla)

            c.showPage()
        c.save()
    if salidamediacarta:
        p1 = Popen(["lp","-dlpfacil",ruta], stdout=PIPE)
    else:
        p1 = Popen(["lp","-dlpfacil_carta","-o","media=Letter",ruta], stdout=PIPE)
    p1.wait()
    result = ( p1.communicate()[0] )
    p1.stdout.close()
    #os.remove(ruta)
    if salidamediacarta:
        result +="media carta"
    
    result +="Impreso.." + idpedido


    return result #dict(result=result,ruta=ruta,consulta=consulta_pedido)#,fecha=consulta_pedido.fentrega.strftime('%m/%d/%Y',x=X)


def grilla():
    tmp_uuid = uuid.uuid4()
    ruta = os.path.join(request.folder,"temp","%s.pdf"%tmp_uuid)
    
    #c = canvas.Canvas(ruta, pagesize=landscape(letter))
    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter
    salidamediacarta=False
    c.setFont("Helvetica",5)

    ancho = int ((width /cm) / .5) 
    posx=0
    for paso in range (0, ancho):
        
        c.line(posx, 0 , posx ,  height)        
        c.drawString(posx + 2* mm, 1.6 *cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 4.6*cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 6.6*cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 8.6*cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 10.6*cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 12.6*cm, "(%s)"%(posx/cm))
        c.drawString(posx + 2* mm, 14.6*cm, "(%s)"%(posx/cm))
        #c.drawString(posx + 2 * mm, posy + 2* mm, "Posx(%s"%posx)
        posx = posx + .5 * cm

    ancho = int ((height /cm) / .5) 
    posy=0
    for paso in range (0, ancho+1):
        c.line(0,posy , width, posy)        
        c.drawString(1.6 * cm, posy + 2* mm, "Posy(%s)"%(posy/cm))
        c.drawString(6.6 * cm, posy + 2* mm, "Posy(%s)"%(posy/cm))
        c.drawString(12.6 * cm, posy + 2* mm, "Posy(%s)"%(posy/cm))
        posy = posy + .5 * cm
        
        
    c.showPage()
    c.save()
    if salidamediacarta:
        #/
        #p1 = Popen(["lp","-dlpfacil","-o","media=Statement",ruta], stdout=PIPE)
        p1 = Popen(["lp","-dlpfacil",ruta], stdout=PIPE)
    else:
        p1 = Popen(["lp","-dlpfacil_carta",ruta], stdout=PIPE)
    p1.wait()
    result = ( p1.communicate()[0] )
    p1.stdout.close()
    #os.remove(ruta)
    if salidamediacarta:
        result +="media carta"
#    
#    result +="Impreso.." + idpedido


    return dict(cm =cm, ruta=ruta,width=width, ancho =ancho,posx=posx)
