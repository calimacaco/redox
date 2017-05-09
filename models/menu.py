# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
    ]

#if auth.user_id:
if auth.has_membership("Administradores"):
    response.menu +=[

        (T('Parametros'), False, "#", [(T('Estados'), False, URL('estadopedido', 'index'), []),
                                       (T('Caracterizacion'), False, URL('caracterizacion', 'index'), []),
                                       LI(_class="divider"),
                                       (T('Subir archivo Zona de Venta'), False, URL('subirventas', 'index'), []),
                                       (T('Subir archivo Grupo Venta'), False, URL('subirventas', 'grupoventas'), []),
                                       (T('Subir archivo Vendedores'), False, URL('subirventas', 'vendedores'), []),
                                       ]),
        ]

if auth.has_membership("Administradores") or auth.has_membership("Vendedores"):
    response.menu +=[
        (T('Ventas'), False, "#", [(T('Vendedores'), False, URL('vendedores', 'index'), []),
                                  ]),
        (T('Pedidos'), False, "#", [(T('Control'), False, URL('pedidos', 'index'), [])
                                   ]),

        ]


if "auth" in locals():
    auth.wikimenu()
