# -*- coding: utf-8 -*-
# intente algo como
def index(): 
    formulario=db(db.tbl_estado).select()
    return dict(formulario=formulario)

def adicionar():
    formulario=SQLFORM(db.tbl_estado)
    if formulario.process().accepted:
        session.flash = 'Estado adicionado' 
        redirect(URL('index'))

    return dict(formulario=formulario)

def editar():
    idregistro=request.args(0) or redirect(URL('index'))
    formulario=SQLFORM(db.tbl_estado,idregistro,showid=False)
    formulario.add_button('Volver',URL('index'))
    if formulario.process().accepted:
        session.flash = 'Se modifico regristro'
        redirect(URL('index'))
    elif formulario.errors:
        response.flash = 'El formulario tiene errores'

    return dict(formulario=formulario)
