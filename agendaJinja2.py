import cgi
import os
from google.appengine.api import users
from models import Persona
from agendakey import agendaKey
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('views'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
		template = JINJA_ENVIRONMENT.get_template('frmAgregarPersona.html')

		template_values = {}

		#Renderizamos la pagina con los valores del servidor
		self.response.write(template.render(template_values))

class PersonaPage(webapp2.RequestHandler):
    def get(self):
        consulta = Persona.query(ancestor = agendaKey('agendaORT')).order(Persona.nombre)
        personas = consulta.fetch(10)

		#Obtenemos el usuario actual. Si es nulo, no esta logueado.
        loggedUser = users.get_current_user()
        if loggedUser:
            nombreUsuario = users.get_current_user().email()
            usuarioUrl = users.create_logout_url(self.request.uri)
            urlText = 'Logout'
        else:
            nombreUsuario = 'No logueado'
            usuarioUrl = users.create_login_url(self.request.uri)
            urlText = 'Login'

        template = JINJA_ENVIRONMENT.get_template('agenda.html')

        template_values = { 'listaPersonas':personas,
                            'usuario':nombreUsuario,
                            'url': usuarioUrl,
                            'textoLink': urlText}
        self.response.write(template.render(template_values))

class AgendaPage(webapp2.RequestHandler):
    def post(self):
        nombreP = cgi.escape(self.request.get('nombre'))
        edadP =  int(cgi.escape(self.request.get('edad')))
        emailP = cgi.escape(self.request.get('email'))

        personaNueva = Persona(parent = agendaKey('agendaORT'))
        personaNueva.nombre = nombreP
        personaNueva.edad = edadP
        personaNueva.email = emailP

        key = personaNueva.put()

        self.redirect('/listarPersonas')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/agregarPersona', AgendaPage),
    ('/listarPersonas', PersonaPage),
], debug=True)
