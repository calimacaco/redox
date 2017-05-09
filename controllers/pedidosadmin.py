# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

@auth.requires_membership('Administradores')
def index():
    fechahoy = datetime.now().date()
    pagina=request.args(0) or 1
    grupoventa=request.args(1) or None
    if pagina <1:
        pagina=1
    formulario=db(db.tbl_pedido.id>0).count()
    paginador, rangoinicio, rangofin =funpaginador(pagina, formulario, 50)
    formulario=db(db.tbl_pedido).select(orderby=db.tbl_pedido.fechasis|db.tbl_pedido.estado,limitby=(rangoinicio,rangofin) )
        
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

    paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-forward" aria-hidden="true"></span>'), _href=URL('index',args=rangofin))))
    rangoinicio=(pagina -1) * maxlinea
    rangofin=rangoinicio + maxlinea

    return paghtml,rangoinicio,rangofin
