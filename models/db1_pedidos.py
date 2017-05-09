# -*- coding: utf-8 -*-

db.define_table('tbl_estado',
                Field('descripicion', 'string',requires=IS_NOT_EMPTY()),
                format="%(descripicion)s"
    )

db.define_table('tbl_caracterizacion',
                Field('descripcion', 'string')
               )

#datos cliente
db.define_table ('tbl_cliente',
                Field('nombre'),
                Field('contacto'),
                Field('nit'),
                Field('direccion'),
                Field('ciudad'),
                Field('telefono'),
                #Field('sucursal','integer'),
                format='%(nombre)s'
                 )

        #entrega
db.define_table('tbl_envio',
        Field('idcliente','reference tbl_cliente'),
        Field('ptoenvio'),
        Field('direnvio'),
        Field('ciudadenvio'),
        Field('contactopto'),
        Field('telpto'),
        Field('dcoalterno')
              )



#nota Subirgrpventas es afectado por algun cambio de la definicio
db.define_table('tbl_grupoventas',
        Field ('nombre'),
        #format="(%nombre)s"
           )

#Vendedor
db.define_table('tbl_usrventas',
        Field ('idgrpventa','reference tbl_grupoventas'),
        Field ('idvendedor','reference auth_user')
        )

#ajuste nombre x vendedor
db.define_table('tbl_vendedor',
                Field ('nombrespool'),
                Field ('idvendedor','reference auth_user')
                )

#nota Subirzonaventas es afectado por algun cambio de la definicio
db.define_table('tbl_zonaventas',
        Field ('nombre'),
        format="%(nombre)s"
        )


#condicion
#db.define_table('tbl_condicion',
#        Field('ordencompra'),
#        Field('condpago'),
#        Field('zona'),
#        )

#pedido
db.define_table('tbl_pedido',
        Field('idcliente','reference tbl_cliente',label ="Nombre del Cliente"),
        Field('nropedido'),
        Field('fecha','date',label="Fecha Pedido"),
        Field('fentrega','date',label="Fecha Entrega"),
        Field('hora'),
        Field('fechasis','datetime',label="Fecha Ingreso"),
        Field('idvendedor','reference auth_user'),
        Field('idenvio','reference tbl_envio'),
        Field('estado','reference tbl_estado'),
        Field('totalbruto','decimal(11,2)',label='Total Bruto'),
        Field('dscoxlinea','decimal(11,2)',label='Desc. x Linea'),
        Field('dsctglobal','decimal(11,2)',label='Desc. Global'),
        Field("porcenglobal",label = "Procentaje Global"),
        Field('subtotal','decimal(11,2)',label='SubTotal'),
        Field('valoriva','decimal(11,2)',label='IVA'),
        Field('impocnsumos','decimal(11,2)',label='Imp. Consumo'),
        Field('total','decimal(11,2)',label='Total'),
        Field('ordencompra'),
        Field('condpago'),
        Field('zona','reference tbl_zonaventas'),
        Field('elaborado'),
        auth.signature,
        format="%(nropedido)s"
        )

db.define_table('tbl_observaciones',
		Field('idpedido','reference tbl_pedido'),
		Field('observacion','text')
    )
db.define_table('tbl_caracterizaciones',
        Field('idcaracterizacion', 'reference tbl_caracterizacion'),
        Field('idpedido', 'reference tbl_pedido'),
       )

db.define_table('tbl_traficopedido',
                Field('idpedido','reference tbl_pedido'),
                Field('idsusario','reference auth_user'),
                Field('estado','reference tbl_estado'),
                Field('fechas','datetime',label="Fecha Ingreso"),
            )

db.define_table('tbl_itempedido',
                Field('idpedido','reference tbl_pedido'),
                Field('referencia'),
                Field('decripcion'),
                Field('um',label="Unidad de Medida"),
                Field('bodega'),
                Field('cantped','integer',label="Cantidad Pedida"),
                Field('catcomp','integer',label="Cantidad Comprometida"),
                Field('catpte','integer',label="Cantidad Penditente"),
                Field('cansep1','integer',label="Cantidad Separada 1"),
                Field('cansep2','integer',label="CantidaSeparada 2"),
                Field('precio','decimal(11,2)',label="Precio Unitario"),
                Field('total','decimal(11,2)',label="Valor Total"),
                Field('iva',label="IVA Por.")
)
