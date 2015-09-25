from google.appengine.ext import ndb

def agendaKey(nombreAgenda):
    #El datastore se creara para entidades de tipo Agenda, con el nombreAgenda indicado
    return ndb.Key('Agenda', nombreAgenda)
