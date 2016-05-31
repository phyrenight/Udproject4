from google.appengine.ext import ndb


class User(ndb.Model):
   # name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)


class Game(ndb.Model):
	# player = ndb.StringProperty(required=True kind='User')
	word = ndb.StringProperty()
	progress = ndb.StringProperty()  # hidden word displaying the parts
	                                 # that have been guessed right
	guesses = ndb.IntegerProperty()    # number of incoorect guesses
	lettersUsed = ndb.StringProperty()  # list of all letters used so far this game
