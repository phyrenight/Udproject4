from google.appengine.ext import ndb

class User(ndb.model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    # currentWord = ndb.StringProperty()
    # currentHiddenWord = ndb.StringProperty()


class Game(ndb.Model):
	# player = ndb.StringProperty()
	word = ndb.StringProperty()
	progress = ndb.StringProperty()  # hidden word displaying the parts
	                                 # that have been guessed right
	guesses = ndb.IntegerProperty()    # number of incoorect guesses
	lettersUsed = ndb.StringProperty()  # list of all letters used so far this game
