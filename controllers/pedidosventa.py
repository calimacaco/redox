# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import os
@auth.requires_membership('Administradores','Vendedores')
def verorden():
    if len(request.args(0)) <1:
        redirect (URL('index'))
    idorden =request.args(0)
    items_pedido=db(db.tbl_itempedido.idpedido==idorden).select()
    return locals()

@auth.requires_membership('Administradores','Vendedores')
def index():
    fechahoy = datetime.now().date()
    pagina=request.args(0) or 1
    vendedores,nomgrupo=pedidostogrupo()
    if pagina <1:
        pagina=1
    consulta=db.tbl_pedido.idvendedor.belongs(vendedores)
    formulario=db(consulta).count()
    #formulario=db(db.tbl_pedido.id>0).count()
    paginador, rangoinicio, rangofin =funpaginador(pagina, formulario, 50)
    formulario=db(consulta).select(orderby=db.tbl_pedido.fechasis|db.tbl_pedido.estado,limitby=(rangoinicio,rangofin))
    return locals()



def funpaginador(pagina,cantidad,maxlinea=10):
    pagina=int(pagina)
    lineaspags=cantidad / maxlinea
    paghtml=UL(_class="pagination")
    if pagina >1:
        paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-backward" aria-hidden="true"></span>'), _href=URL('index',args=pagina-1))))
    if lineaspags> 10:
        rangofin=pagina + 10
    else:
        rangofin=lineaspags
    for pag in range(pagina, rangofin):
        paghtml.append (LI(A(pag, _href=URL('index',args=pag))) )

    if int(lineaspags) >0 :
        paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-forward" aria-hidden="true"></span>'), _href=URL('index',args=rangofin))))
        
    rangoinicio=(pagina -1) * maxlinea
    rangofin=rangoinicio + maxlinea

    return paghtml,rangoinicio,rangofin

@auth.requires_membership('Administradores','Vendedores')
def pedidostogrupo():
    '''
    Busca los vendedores asociados al mismos grupo que el usuario login
    Devuelve una lista de vendedores. si no hay asocio a grupo se devuelve
    el mismo id.login
    '''
    salida=[]
    grupoventa=db(db.tbl_usrventas.idvendedor==auth.user.id).select().first()
    if grupoventa:
        nomgrupo=grupoventa.idgrpventa.nombre
        grupoventa=db(db.tbl_usrventas.idgrpventa==grupoventa.idgrpventa).select(db.tbl_usrventas.idvendedor)
        for vendedor in grupoventa:
            salida.append(vendedor.idvendedor)
    else:
        nomgrupo="Sin Grupo de ventas!!"
        salida.append(auth.user.id)
    return salida,nomgrupo
