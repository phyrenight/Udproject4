import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint

lst = ["cat", "carp", "king"]

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
    	letter = "{}".format(request.name)
        return Response(response=letter)

    @endpoints.method(REQUEST_WORD, Response, path="word_given", http_method="GET", name="user_word")
    def wordGiven(self, choice):
    	words = "{}".format(choice.name)
    	return Response(response=words)

    @endpoints.method(message_types.VoidMessage, Response, path="new_game", http_method="Get", name="new_game")
    def newGame(self, choice):
        """ starts the game
        returns the hiddenWord
        """
        word = getWord()
        #hiddenWord = hideWord(word)
        return Response(response=word)


def getWord():
	length = len(lst)
	num = randint(0,length)
	word = lst[num]
	return word


APPLICATION = endpoints.api_server([hangmanApi])