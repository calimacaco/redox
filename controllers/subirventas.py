# -*- coding: utf-8 -*-
# try something like
import os
@auth.requires_membership('Administradores')
def index():
    formulario = SQLFORM.factory(Field('archivo', 'upload', uploadfolder=os.path.join(request.folder, 'static/temp'))   )
    busqueda = SQLFORM.grid(db.tbl_zonaventas, deletable=False, orderby=db.tbl_zonaventas.nombre, paginate=10)
    #db(db.tbl_zonaventas).select(orderby=db.tbl_zonaventas.nombre)
    if formulario.process().accepted:
        response.flash = 'formulario aceptado'
        nomb_arch=os.path.join(request.folder, 'static/temp',formulario.vars.archivo)
        archivo = open (nomb_arch,'r')
        if not os.path.isfile(nomb_arch):
            session,flash="No se ha seleccionado archivo"
            redirect(ULR("grupoventas"))
        for linea in archivo.readlines():
            linea=linea.replace('\r','')
            linea=linea.replace('\n','')
            linea=linea.strip()
            if len(linea)==0:
                #no se sube linea en blanco
                continue
            busqueda = db(db.tbl_zonaventas.nombre==linea).count()
            #print busqueda
            if (busqueda==0):
                resultado = db.tbl_zonaventas.insert(nombre=linea)
        archivo.close()
        os.remove(nomb_arch)
        response.flash = 'Archivo procesado'

    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    return dict(formulario=formulario, busqueda=busqueda)

@auth.requires_membership('Administradores')
def grupoventas():
    formulario = SQLFORM.factory(Field('archivo', 'upload', uploadfolder=os.path.join(request.folder, 'static/temp'))   )
    busqueda = SQLFORM.grid(db.tbl_grupoventas, deletable=False, orderby=db.tbl_grupoventas.nombre, paginate=10)
    grupovent=db(db.tbl_grupoventas).select(orderby=db.tbl_grupoventas.nombre)
    
    if formulario.process().accepted:
        response.flash = 'formulario aceptado'
        nomb_arch=os.path.join(request.folder, 'static/temp',formulario.vars.archivo)
        if not os.path.isfile(nomb_arch):
            session,flash="No se ha seleccionado archivo"
            redirect(ULR("grupoventas"))
        archivo = open (nomb_arch,'r')
        for linea in archivo.readlines():
            linea=linea.replace('\r','')
            linea=linea.replace('\n','')
            linea=linea.strip()
            if len(linea)==0:
                #no se sube linea en blanco
                continue
        
            if grupovent:
                if  not grupovent.find(lambda registro: linea in registro.nombre):
                        db.tbl_grupoventas.insert(nombre=linea)
            else:
                db.tbl_grupoventas.insert(nombre=linea)
        archivo.close()
        os.remove(nomb_arch)
        #session.flash = 'Archivo procesado'
        redirect(URL("grupoventas"))

    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    return dict(formulario=formulario, busqueda=busqueda)

@auth.requires_membership('Administradores')
def vendedores():
    formulario = SQLFORM.factory(Field('archivo', 'upload', uploadfolder=os.path.join(request.folder, 'static/temp')))
    grupoventas=db(db.tbl_grupoventas).select()

    id_grupo=db(db.auth_group.role=="Vendedores").select(db.auth_group.id).first()
    id_grupo=id_grupo.id
    busqueda = (db.auth_membership.group_id==id_grupo) &(db.auth_user.id==db.auth_membership.user_id)
                                                                        
    busqueda = SQLFORM.grid(busqueda, deletable=False, paginate=10)
    
    if formulario.process().accepted:
        #esponse.flash = 'formulario aceptado'
        nomb_arch=os.path.join(request.folder, 'static/temp',formulario.vars.archivo)
        if not os.path.isfile(nomb_arch):
            session.flash = 'No se a seleccionado archivo'
            redirect(URL("grupoventas"))

        archivo = open (nomb_arch,'r')
        for linea in archivo.readlines():
            linea=linea.replace('\r','')
            linea=linea.replace('\n','')
            linea=linea.strip()
            campos =linea.split(',')
            
            if len(campos) <5: #No tiene las columnas suficientes!!! no se procesa
                continue
            idgrpventa=0
            for registro in grupoventas.find(lambda registro: registro.nombre==campos[4]):
                idgrpventa=registro.id
                break
            if  idgrpventa==0:
                #"No existe el grupo -- No se registra el vendedor!!"
                continue
            if db(db.auth_user.username==campos[0]).select():
                 #ya existe no se sube el vendedor
                animal="vendedor existe"    

                continue
            animal="aqui1"

            idvendedor = db.auth_user.insert(username=campos[0],
                                    first_name=campos[1].decode('latin-1') + " " + campos[2].decode('latin-1'),
                                    password=str(CRYPT(salt=True)(campos[3])[0])
                          )
            usrgrupo=db.tbl_usrventas.insert(idgrpventa=idgrpventa, idvendedor=idvendedor)
            db.auth_membership.insert(user_id=idvendedor,group_id=id_grupo)
        #animal="fin"
        archivo.close()
        os.remove(nomb_arch)
        session.flash = 'Archivo procesado'
        redirect(URL("vendedores"))
    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    return dict(formulario=formulario, busqueda=busqueda)
