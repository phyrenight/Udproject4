import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

REQUEST_LETTER = endpoints.ResourceContainer(
	message_types.VoidMessage,
	name = messages.StringField(1),
)
REQUEST_WORD = endpoints.ResourceContainer(
	name = messages.StringField(1),
)
package = "response"

class Response(messages.Message):
    response = messages.StringField(1)

@endpoints.api(name = 'hangmanEndPoints', version='1')
class hangmanEndPoints(remote.Service):

    @endpoints.method(REQUEST_LETTER, Response, path = "letter_given", http_method = "GET", name = "letter")
    def letterGiven(self, choice):
    	letter = "{}".format(choice.name)
        return Response(response=letter)

    @endpoints.method(REQUEST_WORD, Response, path="word_given", http_method="GET", name="user_word")
    def wordGiven(self, choice):
    	words = "{}".format(choice.name)
    	return Response(response=words)




APPLICATION = endpoints.api_server([hangmanEndPoints])