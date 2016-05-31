import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint
import random
import string
from models import Game, User
import hashlib
lst = ["cat", "carp", "king"]
word = "hello"



REQUEST_LETTER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    name = messages.StringField(1),
)
REQUEST_WORD = endpoints.ResourceContainer(
    name = messages.StringField(1),
)

REQUEST_NEW_GAME = endpoints.ResourceContainer(
    message_types.VoidMessage,
    )

REGISTER_USER = endpoints.ResourceContainer(
  #  user = messages.StringField(1),
    pwd = messages.StringField(2),
    verifyPwd = messages.StringField(3),
    email = messages.StringField(4),
    )

class Response(messages.Message):
    response = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    lettersUsed = messages.StringField(4)

class NewGame(messages.Message):
    word = messages.StringField(1)
    progress = messages.StringField(2)
    guess = messages.IntegerField(3)
    lettersUsed = messages.StringField(4)

class RegisterUser(messages.Message):
    response = messages.StringField(1)



@endpoints.api(name='hangmanEndPoints', version='v1')
class hangmanApi(remote.Service):
    game  = Game(word="Cat", progress="***", lettersUsed="", guesses=0)
    game.put()

    
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
    
    """
    @endpoints.method(REQUEST_WORD, Response, path="word_given", http_method="GET", name="user_word")
    def wordGiven(self, choice):
        if choice.name is None:
            return Response(response="nothing was entered")
        words = "{}".format(choice.name)
        if  words.isalpha() is False or len(words) < 2:
           return Response(response="Please enter a word.")
        else:
            return Response(response="not in the word")
    """    

    
    @endpoints.method(message_types.VoidMessage, NewGame, path="new_game", http_method="Get", name="new_game")
    def newGame(self, choice):
        """ 
            args: choice - contains the users guessed letter
            starts the game
            returns the hiddenWord
        """
        word = getWord()
        hiddenWord = hideWord(word)
        game = Game(word=word, progress=hiddenWord, guesses=0, lettersUsed="")
        game.put()
        return NewGame(word=game.word, progress=game.progress,
                       guess=game.guesses, lettersUsed=game.lettersUsed)

    @endpoints.method(REGISTER_USER, RegisterUser, path='register_User', http_method="POST", name='register_User')
    def UserRegister(self, request):
  
      #  print request.user
        print request.pwd
        print request.verifyPwd
        print request.email
        if request.pwd == request.verifyPwd:
            user = User()
            user.email = request.email
            user.password = self.encrypt(request)
            user.put()
            return RegisterUser(response="New user registered")
        else:
            return RegisterUser(response="Please make sure your passwords match.")
    
    @endpoints.method()
    def Userlogin():
        pass

    def encrypt(self, request):
        self.salt = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(5))
        self.passwordHash = hashlib.sha256(request.email + request.pwd + self.salt).hexdigest() 
        return " %s,%s" % (self.passwordHash, self.salt)
  
    def cancel_game():
        pass

def getWord():
    """
        gets a word from the word bank
    """
    length = len(lst)
    num = randint(0,(length-1))
    word = lst[num]
    return word


def hideWord(word):
    """
        args: word - user
        hides the word so the user can guess it.
    """
    length = len(word)
    hidden = '*'*length
    return hidden

 
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


"""
# may be deleted haven't decided
def hitOrMissWord(guess):
    "
        args: guess - contains the users guessed 
        checks to see if word guess was right.
    "
    if guess == word:
        return "You guessed the word: {}".format(word)
    else:
        incorrectGuess += 1
        return "you guessed wrong."
"""
def genericHangman():
    """
       generic images for hangman progress.
    """ 
    if incorrectGuess == 0:
        return """
             ______
             |    |
             |
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrectGuess == 1:
        return """
             ______
             |    |
             |    o
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrectGuess == 2:
        return """
             ______
             |    |
             |    o
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrectGuess == 3:   
        return  """
            ______
            |    |
            |    o
            |    |
            |
            |
            |
         |--------|
        """

    elif incorrectGuess == 4:
        return """
            ______
            |    |
            |    o
            |   /|
            |
            |
            |
        |--------|
        """
    
    elif incorrectGuess == 5:
        return """
            ______
            |    |
            |    o
            |   /|\
            |
            |
            |
        |--------|
        """

    elif incorrectGuess == 6:
        return """
            ______
            |    |
            |    o
            |   /|\
            |   /
            |
            |
        |--------|
        """

    else:
        return """
            ______
            |    |
            |    o
            |   /|\
            |   / \
            |
            |
        |--------|
        """
    


"""


    @endpoints.method()
    def Userlogout():
        pass
"""

APPLICATION = endpoints.api_server([hangmanApi])