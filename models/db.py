# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

auth.settings.extra_fields['auth_user']= [
  Field('direccion'),
  Field('ciudad'),
  Field('telefono'),
  Field('celular'),
  Field('sexo',requires=IS_IN_SET((T('masculino'),T('femenino')))),
  Field('nacimiento','date',label='Fecha de Nacimiento')
 ]

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


###Mensajes:
###Mensajes del sistema
auth.messages.submit_button = 'Enviar'
auth.messages.verify_password = 'Verificar Contraseña'
auth.messages.new_password = 'Nueva contraseña'
auth.messages.old_password = 'Contraseña anterior'
auth.messages.password_changed = 'Contraseña cambiada'
auth.messages.retrieve_username = 'Su nombre de usuario es: %(username)s'
auth.messages.invalid_login = 'Inicio de sesión inválido'
auth.messages.invalid_user = 'Usuario inválido'
auth.messages.mismatched_password = 'Los campos de contraseña no coinciden'
auth.messages.new_password_sent = 'Una nueva contraseña le fue enviada por correo'
auth.messages.delete_label = 'Marcar para borrar:'
auth.messages.function_disabled = 'Función deshabilitada'
auth.messages.access_denied = 'Privilejios insuficientes'
auth.messages.registration_verifying = 'Ud. no ha confirmado suregistro (email de verificación)'
auth.messages.registration_pending = 'Registration is pending approval'
auth.messages.login_disabled = 'Login deshabilitado por el administrador'
auth.messages.logged_in = 'Logged in'
auth.messages.email_sent = 'Email enviado'
auth.messages.unable_to_send_email = 'No es posible enviar el email'
auth.messages.email_verified = 'Email verificado'
auth.messages.logged_out = 'Finalizó la sesión'
auth.messages.registration_successful = 'Registro satifsfactorio'
auth.messages.invalid_email = 'Inválido: email'
auth.messages.unable_send_email = 'No es posible enviar el email (2)'
auth.messages.invalid_login = 'Inválido login'
auth.messages.invalid_user = 'Inválido user'
auth.messages.is_empty = "No puede ser vacío"
auth.messages.mismatched_password = "Las contraseñas con coinciden"
auth.messages.username_sent = 'Your username was emailed to you'
auth.messages.new_password_sent = 'A new password was emailed to you'
auth.messages.password_changed = 'Contraseña actualizada'
auth.messages.new_password = 'Nueva contraseña'
auth.messages.old_password = 'Contraseña Anterior'

auth.messages.retrieve_username = 'Your username is: %(username)s'
auth.messages.retrieve_username_subject = 'Username retrieve'
auth.messages.retrieve_password = 'Your password is: %(password)s'
auth.messages.retrieve_password_subject = 'Password retrieve'
auth.messages.invalid_reset_password = 'Invalido reset password'
auth.messages.profile_updated = 'Perfil actualizado'
auth.messages.group_description ='Group uniquely assigned to user %(id)s'
auth.messages.register_log = 'User %(id)s Registered'
auth.messages.login_log = 'User %(id)s Logged-in'
auth.messages.logout_log = 'User %(id)s Logged-out'
auth.messages.profile_log = 'User %(id)s Profile updated'
auth.messages.verify_email_log = 'User %(id)s Verification email sent'
auth.messages.retrieve_username_log = 'User %(id)s Username retrieved'
auth.messages.retrieve_password_log = 'User %(id)s Password retrieved'
auth.messages.reset_password_log = 'User %(id)s Password reset'
auth.messages.change_password_log = 'User %(id)s Password changed'
auth.messages.add_group_log = 'Group %(group_id)s created'
auth.messages.del_group_log = 'Group %(group_id)s deleted'
auth.messages.add_membership_log = None
auth.messages.del_membership_log = None
auth.messages.has_membership_log = None
auth.messages.add_permission_log = None
auth.messages.del_permission_log = None
auth.messages.has_permission_log = None
auth.messages.label_first_name = 'First name'
auth.messages.label_last_name = 'Last name'
auth.messages.label_username = 'Usuario'
auth.messages.label_email = 'E-mail'
auth.messages.label_password = 'Contrasena'
auth.messages.label_registration_key = 'Registration key'
auth.messages.label_reset_password_key = 'Reset Password key'
auth.messages.label_registration_id = 'Registration identifier'
auth.messages.label_role = 'Role'
auth.messages.label_description = 'Description'
auth.messages.label_user_id = 'User ID'
auth.messages.label_group_id = 'Group ID'
auth.messages.label_name = 'Name'
auth.messages.label_table_name = 'Table name'
auth.messages.label_record_id = 'Record ID'
auth.messages.label_time_stamp = 'Timestamp'
auth.messages.label_client_ip = 'Client IP'
auth.messages.label_origin = 'Origin'
auth.messages.label_remember_me = "Recordar por( 30 dias)"
