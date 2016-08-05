from google.appengine.ext import ndb
from protorpc import messages
import sys 

sys.path.insert(0, 'lib')
from wordnik import *


apiUrl = 'http://api.wordnik.com/v4'
apiKey = "2551259012aa25070f29c8321e8f982d5c6999b433b6ab11e"
client = swagger.ApiClient(apiKey, apiUrl)

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)



class Game(ndb.Model):
    # player = ndb.StringProperty(required=True kind='User')
    word = ndb.StringProperty()
    progress = ndb.StringProperty()  # hidden word displaying the parts
                                     # that have been guessed right
    guesses = ndb.IntegerProperty(default=6)    # number of incoorect guesses
    guessesRemaining = ndb.IntegerProperty(default=6)
    lettersUsed = ndb.StringProperty()  # list of all letters used so far this game
    hint = ndb.StringProperty()
    user = ndb.KeyProperty(required=True, kind='User')
    endGame = ndb.BooleanProperty(required=True, default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def hideWord(self, word):
        """
           args - word: random word
           hides the word so the user can guess it.
           return - hidden: a string of *
        """
        self.length = len(word)
        self.hidden = '*'*self.length
        return self.hidden

    @classmethod
    def new_game(cls, user):
        game = Game(user=user,
        	        endGame=False)
        word, definition = cls.getWord(game)
        hidden = cls.hideWord(game, word)
        game.progress = hidden
        game.hint =  definition
        game.word =  word
        game.put()
        return game

    def get_form(self):
        form = NewGameForm()
        form.urlsafeKey = self.key.urlsafe()
        form.userName = self.user.get().name
       # form.message = message
        form.hint = self.hint
        form.word = self.word
        form.progress = self.progress
        return form

    def getWord(self):
        """
            gets a word and the words definition from wordnik.com
            returns - word: a string
                    - definition: definition of the word (a string)
        """
    	wordApi = WordsApi.WordsApi(client)
    	word = wordApi.getRandomWord().word
    	defApi = WordApi.WordApi(client)
    	definition = defApi.getDefinitions(word,
    		                                sourceDictionaries='wiktionary',
    		                                limit=1)[0].text
        return word, definition

class NewGameForm(messages.Message):
    urlsafeKey =  messages.StringField(1, required=True)
    userName = messages.StringField(2, required=True)
    hint = messages.StringField(3, required=True)
#    message = messages.StringField(4, required=True)
    word = messages.StringField(5, required=True)
    progress = messages.StringField(6, required=True)


class Score(ndb.Model):
    player = ndb.StringProperty(required=True)
    score = ndb.IntegerProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    won = ndb.BooleanProperty(required=True)

    def get_form(self):
        score = ScoreForm()
        score.player = self.user.get().name
        score.date = str(self.date)
        score.won = self.won
        score.score = self.score
        return score

class ScoreForm(messages.Message):
    name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    score = messages.IntegerField(4, required=True)

class UsersGames(messages.Message):
    items = messages.MessageField(NewGameForm, 1, repeated=True)

class UserScores(messages.Message):
    items = messages.MessageField(ScoreForm, 1, repeated=True)