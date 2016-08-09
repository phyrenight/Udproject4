import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint
import random
import string
from models import Game, User, Letters
from models import NewGameForm, UsersGames, UserScores
import hashlib
from utils import get_by_urlsafe
lst = ["cat", "carp", "king"]
word = "hello"


# used for returninga value
REQUEST_GAME = endpoints.ResourceContainer(
     urlsafeKey = messages.StringField(1),
)
REQUEST_LETTER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    urlsafeKey = messages.StringField(1),
    letter = messages.StringField(2),
)
REQUEST_WORD = endpoints.ResourceContainer(
    name = messages.StringField(1),
)

REQUEST_NEW_GAME = endpoints.ResourceContainer(
    user_name = messages.StringField(1),
    )

REGISTER_USER = endpoints.ResourceContainer(
    name = messages.StringField(1),
   # pwd = messages.StringField(2),
   # verifyPwd = messages.StringField(3),
    email = messages.StringField(4),
    )

LOGIN_USER = endpoints.ResourceContainer(
    email = messages.StringField(1),
    pwd = messages.StringField(2),
    )


# used for getting values from the user
class ScoreForm(messages.Message):
    player = messages.StringField(1)
    score = messages.IntegerField(2)
    date = messages.StringField(3)

class Response(messages.Message):
    response = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    lettersUsed = messages.StringField(4, repeated=True)

class NewGame(messages.Message):
    word = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    hint = messages.StringField(4)

class SingleMessage(messages.Message):
    response = messages.StringField(1)

@endpoints.api(name='hangmanEndPoints', version='v1')
class hangmanApi(remote.Service): # change to HangManApi

    # write a if statement to test if letter is in lettersUsed before continuing
    @endpoints.method(REQUEST_LETTER, Response, path="game_play/{urlsafeKey}", http_method="GET", name="letter")
    def letterGiven(self, request):
        if request.letter is None: 
            return Response(response="Nothing entered. please enter a letter.")
        else:   
            letter = "{}".format(request.letter)
            if len(letter) > 1 or letter.isalpha() is False:
               return Response(response="Please enter a letter")
            else:
               game_data = get_by_urlsafe(request.urlsafeKey, Game)
               game = Game.query().get()
               n = game.lettersUsed[0]
               print game.lettersUsed[0]
               print game.word
               num = hitOrMissLetter(letter, game)
               return Response(response=num, progress=game.progress,
                               lettersUsed=game.lettersUsed)# Letters(items=[i.get_letter() for i in game.lettersUsed]))
    
    @endpoints.method(REQUEST_NEW_GAME, NewGameForm, path="new_game", http_method="GET", name="new_game")
    def newGame(self, request):
        """ 
            args: choice - contains the users guessed letter
            creates a new game
            returns: user - urlsafekey based off of the users key
                     hint - definitin of the word
                     word - a randomly generated word
                     progress - astericks string that is as long as the word
        """
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                        "That user does not exist")
        game = Game.new_game(user.key)
        return game.get_form("Good luck")

    @endpoints.method(REGISTER_USER, SingleMessage, path='register_User',
                      http_method="POST", name='register_User')
    def UserRegister(self, request):
  
        user = User()
        user.name = request.name
        user.email = request.email
        user.put()
        return SingleMessage(response="New user registered")
     
    @endpoints.method(REQUEST_GAME, NewGameForm, path='cancel_game/{urlsafeKey}', http_method="POST",
                     name='cancel_game')
    def CancelGame(self, request):
        game = get_by_urlsafe(request.urlsafeKey, Game)
        if game.endGame:
            return game.to_form('game already ended.')
        else:
            game.end_game = True
            game.put()
            return game.get_form('game_cancelled.')

    @endpoints.method(REQUEST_WORD, UsersGames, path='game_history/{name}', name='user_history', http_method="GET")
    def get_history(self,request):
       # try:
        print request.name
        user = User.query(User.name == request.name).get()
        print user.key
        games = Game.query(Game.user == user.key)
        #print games.user
        return UsersGames(items=[i.get_form() for i in games]) # Game.query(Game.user == user.key)])
        #except:
           # print "user not found"
           # pass

    @endpoints.method(REQUEST_GAME, NewGameForm, path='game/{urlsafeKey}', http_method='GET', name='game')
    def get_game(self, request):
        """
            gets a single game
        """
        # add try  incase game does not exist 
        # think of adding a check so only game owner can access game
        # add check to maek sure game is active
        game = get_by_urlsafe(request.urlsafeKey, Game) 
        return game.get_form() # "game retrieved") fix this should take a message or not???

    @endpoints.method(REQUEST_WORD, UserScores, path='score/{name}', http_method='GET', name='user_score')
    def get_user_score(self, request):
        try:
            user = User.query(User.name == request.name).get()
            userScores = Score.query(Score.player == user.name)
            return UserScores(items=[i.get_form() for i in Score.query(Score.Player == request.user)])
        except:
            pass    
"""
    @endpoints.method()
    def get_high_score(self, request):
        highScore = Score.query()
"""
def hitOrMissLetter(letter, game):
    """
       args: letter- user's letter guess
       checks to see if the word contains the guesses letter.
       returns: a message if you passsed or failed.
    """
    maxGuess = 6
    guess = game.lettersUsed
    if game.lettersUsed[0] is None:
        print "hello"
        game.lettersUsed = [] 
    game.lettersUsed.append(letter) # place holder till letterUsed can be changed to a ListProperty 
    print game.lettersUsed
    # update used letter bank to include letter
    if game.word.find(letter) > -1:
        lst = list(game.progress)
        place = 0
        for i in game.word:
            if i == letter:
                lst[place] = i
            place += 1
        game.progress = "".join(lst)
        if game.progress == game.word:
            return "You have guessed the word."
        else:
            game.put()
            return "{} was found in the word".format(letter)

    else:
        game.guesses += 1
        if game.guesses == maxGuess:
            return "you have failed to guess this word."
        else:
            return "{} is not in the word. ".format(game.lettersUsed)




APPLICATION = endpoints.api_server([hangmanApi])
