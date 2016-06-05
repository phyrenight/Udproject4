import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint
import random
import string
from models import Game, User
from models import NewGameForm
import hashlib
lst = ["cat", "carp", "king"]
word = "hello"


# used for returninga value
REQUEST_LETTER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    name = messages.StringField(1),
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
class Response(messages.Message):
    response = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    lettersUsed = messages.StringField(4)

class NewGame(messages.Message):
    word = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    hint = messages.StringField(4)

class SingleMessage(messages.Message):
    response = messages.StringField(1)

@endpoints.api(name='hangmanEndPoints', version='v1')
class hangmanApi(remote.Service):

    # write a if statement to test if letter is in lettersUsed before continuing
    @endpoints.method(REQUEST_LETTER, Response, path="letter_given", http_method="GET", name="letter")
    def letterGiven(self, request):
        if request.name is None: 
            return Response(response="Nothing entered. please enter a letter.")
        else:   
            letter = "{}".format(request.name)
            if len(letter) > 1 or letter.isalpha() is False:
               return Response(response="Please enter a letter")
            else:
               num = hitOrMissLetter(letter, self.game)
               return Response(response=num)
    
    @endpoints.method(REQUEST_NEW_GAME, NewGameForm, path="new_game", http_method="Get", name="new_game")
    def newGame(self, request):
        """ 
            args: choice - contains the users guessed letter
            starts the game
            returns the hiddenWord
        """
        print request.user_name
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                        "That user does not exist")
        game = Game.new_game(user.key)
        return game.get_form()

    @endpoints.method(REGISTER_USER, SingleMessage, path='register_User', http_method="POST", name='register_User')
    def UserRegister(self, request):
  
        user = User()
        user.name = request.name
        user.email = request.email
        user.put()
        return SingleMessage(response="New user registered")

    
    def CancelGame(self,):
        pass

def getWord():
    """
        gets a word from the word bank
    """
    length = len(lst)
    num = randint(0,(length-1))
    word = lst[num]
    return word

def hitOrMissLetter(letter, game):
    """
       args: letter- user's letter guess
       checks to see if the word contains the guesses letter.
       returns: a message if you passsed or failed.
    """
    maxGuess = 6
    guess = game.lettersUsed
    game.lettersUsed = guess + " " + letter # place holder till letterUsed can be changed to a ListProperty 
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