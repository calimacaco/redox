# -*- coding: utf-8 -*-
# try something like
def index(): 
    formulario=db(db.tbl_caracterizacion).select()
    return dict(formulario=formulario)
