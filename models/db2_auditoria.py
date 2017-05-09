# -*- coding: utf-8 -*-
db.define_table('tbl_audit_pedido',
        Field('idcliente','reference tbl_cliente'),
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
        auth.signature
        )

db.define_table('tbl_audit_observaciones',
		Field('idpedido','reference tbl_pedido'),
		Field('observacion','text'),
        auth.signature
                )

db.define_table('tbl_audit_itempedidos',
                Field('idpedido','reference tbl_audit_pedido'),
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
                Field('iva',label="IVA Por."),
                auth.signature
)
