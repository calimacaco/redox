# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index():
    pagina=request.args(0) or 1
    grupoventa=request.args(1) or None
    
    if pagina <1:
        pagina=1
    
    if grupoventa:
        busqueda = db.tbl_usrventas.idgrpventa==grupoventa
        paginador, rangoinicio, rangofin =fun_paginador(pagina, busqueda)
        formulario=db(busqueda).select(limitby=(rangoinicio, rangofin))
    else:
        idventas =db(db.auth_group.role=="Vendedores").select(db.auth_group.id).first()
        busqueda=db.auth_membership.group_id==idventas.id
        paginador, rangoinicio, rangofin =fun_paginador(pagina, busqueda)
        formulario=db(db.auth_membership.group_id==idventas.id).select(limitby=(rangoinicio, rangofin))

    return dict(formulario=formulario,paginador=paginador,grupoventa=grupoventa)

@auth.requires_login()
def grupoventas():
    formulario= db(db.tbl_grupoventas).select()
    return dict(formulario=formulario)




def fun_paginador(idpagina,busqueda):
    maxlinea=10
    idpagina=int(idpagina)
    cantidad= db(busqueda).count()
    lineaspags=cantidad / maxlinea
    paghtml=UL(_class="pagination")
    if idpagina >1:
        paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-backward" aria-hidden="true"></span>'), _href=URL('index',args=idpagina-1))))

    

    if lineaspags>maxlinea:
        rangofin=idpagina + maxlinea
    else:
        rangofin=lineaspags

    for pag in range(idpagina, rangofin):
        paghtml.append (LI(A(pag, _href=URL('index',args=pag))) )

    paghtml.append(LI(A(XML('<span class="glyphicon glyphicon-forward" aria-hidden="true"></span>'), _href=URL('index',args=rangofin))))
    rangoinicio=(idpagina -1) * maxlinea
    rangofin=rangoinicio + maxlinea
    return paghtml,rangoinicio,rangofin
