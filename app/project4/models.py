from google.appengine.ext import ndb

class User(ndb.model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    currentWord = ndb.StringProperty
    currentHiddenWord = ndb.StringProperty()