import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

REQUEST_LETTER = endpoints.ResourceContainer(
	letter = messages.StringField(1),
)
REQUEST_WORD = endpoints.ResourceContainer(
	word = messages.StringField(1),
)

class Response(messages.Message):
    response = messages.StringField(1)

@endpoints.api('hangmanEndPoints', version='1')
class hangmanEndPoints(remote.Service):

    @endpoints.method(REQUEST_LETTER, Response, path="letter_given", http_method="GET", name="letter")
    def letterGiven(self, choice):
        return response(choice=choice)

    @endpoints.method(REQUEST_WORD, Response, path="word_given", http_method="Get", name="user_word")
    def wordGiven(self, choice):
    	return Response(choice)


print 'Content-type: text/plain'
print ''
print 'Hello there Chuck'

APPLICATION = endpoints.api_server([hangmanEndPoints])