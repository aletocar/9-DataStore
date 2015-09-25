from google.appengine.ext import ndb

class Persona(ndb.Model):
    nombre = ndb.StringProperty(indexed=True)
    edad = ndb.IntegerProperty(indexed=False)
    email = ndb.StringProperty()
