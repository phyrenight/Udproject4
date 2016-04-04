import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint

lst = ["cat", "carp", "king"]
word = "hello"
hidden = ""
incorrectGuess = 0
maxGuess = 6

REQUEST_LETTER = endpoints.ResourceContainer(
	message_types.VoidMessage,
	name = messages.StringField(1),
)
REQUEST_WORD = endpoints.ResourceContainer(
	name = messages.StringField(1),
)

REQUEST_NEW_GAME = endpoints.ResourceContainer(
    name = messages.StringField(1),
	)

class Response(messages.Message):
    response = messages.StringField(1)

@endpoints.api(name='hangmanEndPoints', version='v1')
class hangmanApi(remote.Service):


    @endpoints.method(REQUEST_LETTER, Response, path = "letter_given", http_method = "GET", name = "letter")
    def letterGiven(self, request):
        if request.name is None: 
            return Response(response="Nothing entered. please enter a letter.")
        letter = "{}".format(request.name)
        if len(letter) > 1 or letter.isalpha() is False:
            return Response(response="Please enter a letter")
        else:
            num = hitOrMissLetter(letter)
            return Response(response=num)

    @endpoints.method(REQUEST_WORD, Response, path="word_given", http_method="GET", name="user_word")
    def wordGiven(self, choice):
        #words = "{}".format(choice.name)
        if choice.name is None:
            return Response(response="nothing was entered")
        words = "{}".format(choice.name)
        if  words.isalpha() is False or len(words) < 2:
           return Response(response="Please enter a word.")
        else:
            return Response(response="not in the word")
        


    @endpoints.method(message_types.VoidMessage, Response, path="new_game", http_method="Get", name="new_game")
    def newGame(self, choice):
        """ starts the game
        returns the hiddenWord
        """
        word = getWord()
        hiddenWord = hideWord(word)
        return Response(response=hiddenWord)


def getWord():
    length = len(lst)
    num = randint(0,(length-1))
    print num
    word = lst[num]
    return word


def hideWord(word):
    length = len(word)
    hidden = '*'*length
    return hidden

 
def hitOrMissLetter(letter):
	# update used letter bank to include letter
    if word.find(letter) > -1:
        lst = list(hidden)
        place = 0
        for i in word:
            if i == letter:
                lst[place] = i
            place += 1
        hidden = "".join(lst)
        if hidden == word:
        	return "You have guessed the word."
        else:
            return "{} was found in the word".format(letter)
    else:
    	incorrectGuess += 1
        if incorrectGuess == maxGuess
            return "ypu have failed to guess this word."
        else:
    	    return "{} is not in the word. ".format(letter)


def hitOrMissWord(guess):
    if guess == word:
        return "You guessed the word: {}".format(word)
    else:
    	incorrectGuess += 1
    	return "you guessed wrong."


def genericHangman():
    """
       generic images for hangman progress.
    """ 
    if incorrect_guess == 0:
        """
             ______
             |    |
             |
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrect_guess == 1:
        """
             ______
             |    |
             |    o
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrect_guess == 2:
        """
             ______
             |    |
             |    o
             |
             |
             |
             |
         |--------|
        """
    
    elif incorrect_guess == 3:
        
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

    elif incorrect_guess == 4:
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
    
    elif incorrect_guess == 5:
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

    elif incorrect_guess == 6:
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


APPLICATION = endpoints.api_server([hangmanApi])