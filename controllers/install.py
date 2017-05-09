# -*- coding: utf-8 -*-
# try something like
def index(): 
    ################## DEFECTO #################
    creargrupos()
    crearadmin()
    crearestados()
    #caracterizacion()
    
    
def creargrupos():
    if db(db.auth_group).isempty():
        db.auth_group.insert (role="Administradores",description="Grupo dedicado a la parametrizacion  e importar/exporta datos")
        db.auth_group.insert (role="Gerencia",description="Grupo dedicado a ver el comportamiento de los indicadores del sistema")
        db.auth_group.insert (role="Vendedores",description="agrupación de los vendedores")
        db.auth_group.insert (role="Logistica",description="Separadores y empacadores")
        db.auth_group.insert (role="Clientes",description="Consultan el estado del pedido")
        return "ok"

        
def crearadmin():
    if db(db.auth_user).isempty():
        db.auth_user.insert (first_name="Administrador",
                             last_name="Sistema",
                             username="admin",
                             password=str(CRYPT(salt=True)('admin.2017')[0])
                             )
    idamin=db.auth_membership.insert(user_id=1,group_id=1)
    return "ok"
    
def crearestados():
    if db(db.tbl_estado).isempty():
        db.tbl_estado.insert(descripicion="Cancelada")
        db.tbl_estado.insert(descripicion="Retenida")
        db.tbl_estado.insert(descripicion="Ingreso desde CGUNO")
        db.tbl_estado.insert(descripicion="Caracterización")
        db.tbl_estado.insert(descripicion="Impresión")
        db.tbl_estado.insert(descripicion="Separado")
        db.tbl_estado.insert(descripicion="Empaque")
        db.tbl_estado.insert(descripicion="Facturada")
        db.tbl_estado.insert(descripicion="Remisionada")
        db.tbl_estado.insert(descripicion="Transporte")
        db.tbl_estado.insert(descripicion="Finalizada")
    return "ok"

def caracterizacion():
    if db(db.tbl_caracterizacion).isempty():
        db.tbl_caracterizacion.insert(descripcion="Urgente")
        db.tbl_caracterizacion.insert(descripcion="Completo")
        db.tbl_caracterizacion.insert(descripcion="Como Este")
        db.tbl_caracterizacion.insert(descripcion="Transportadora")
        db.tbl_caracterizacion.insert(descripcion="Sabado")
    return "ok"
