# -*- coding: utf-8 -*-
# try something like
def index(): 
    formulario=SQLFORM.grid(db.tbl_cliente)
    return locals()
