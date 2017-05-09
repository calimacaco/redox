# -*- coding: utf-8 -*-
# try something like
import datetime  


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


@auth.requires_login()
def index(): 
    
    if auth.has_membership( 'Administradores',auth.user_id):
        redirect (URL(request.application,'pedidosadmin','index'))
    if auth.has_membership( 'Vendedores',auth.user_id):
        redirect (URL(request.application,'pedidosventa','index'))
    
    vendedor=db(db.auth_user.id==auth.user_id).select().first()
    busqueda=db((db.tbl_pedido.idvendedor==auth.user_id) &
                  (db.tbl_pedido.estado==1) ).select()

    formulario=FORM(TR("Seleccionar pedido:",
          SELECT(_name='selectpedido', 
          *[OPTION(busqueda[i].nropedido, _value=str(busqueda[i].id)) for i in range(len(busqueda))])), 
          TR(INPUT(_type='submit')))
    
    return dict(formulario=formulario,vendedor=vendedor)



def calculofecha():
  return "miau"

@auth.requires_login()
def lst_items():
#  if len(request.args)<1:
#    redirect (URL("index"))
  nropedido=request.args(0,cast=int)

  busqueda=db(db.tbl_pedido.id ==nropedido).select()


  db.tbl_itempedido.id.readable = False
  db.tbl_itempedido.id.writable = False
  db.tbl_itempedido.idpedido.readable = False

  formulario=SQLFORM.grid(db.tbl_itempedido.idpedido==nropedido,
                          user_signature=False,
                          maxtextlength=64,
                          deletable=False,
                          editable=False,
                          details=False,
                          create=False,
                          csv=False)
  return locals()


@auth.requires_login()
def nuevo():
  #db.tbl_pedido.diastrans = Field.Virtual(calculofecha())
    #lambda registro: datetime.datetime.strptime(request.now,"%m - %d  / %Y")
    #)
  if auth.has_membership( 'Administradores',auth.user_id):
    consulta=db.tbl_pedido

  superquery = request.get_vars ['keywords']













  links = [ lambda row: A('items',_class='button btn btn-default',_href=URL("pedidos","lst_items",args=[row.id])),
            lambda row: A(XML('<span class="glyphicon glyphicon-print" aria-hidden="true"></span>'),' Imprmir',
                                _class='btn  btn-xs btn btn-info',
                                callback=URL('impresion','imprimirorden',args=(row.id)),target='estado'),
          ]


  formulario=SQLFORM.grid(consulta,
                          deletable=False,
                          editable=False,
                          details=False,
                          create=False,
                          maxtextlength=64,
                          links=links, 
                          fields=[db.tbl_pedido.nropedido, db.tbl_pedido.idcliente,
                                db.tbl_pedido.fecha,     db.tbl_pedido.fentrega, 
                                db.tbl_pedido.estado   
                                #db.tbl_pedido.diastrans
                                ], 
                          selectable=[('Impresión',lambda ids:  redirect(URL('imprimir',args=ids))),#vars=dict(id=ids)))), # [db.tbl_pedido.id], 'class1'),
                                      ('Caracterizar',lambda ids: [db.tbl_pedido.id], 'class2')]

#                          selectable=lambda ids: [db.tbl_pedido.id]
                          )
  return locals()


def imprimir():
    a="aqui imprimir"

    return locals()