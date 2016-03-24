import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

REQUEST_LETTER = endpoints.ResourceCountainer(
	letter = messages.StringField(1),
)
REQUEST_WORD = endpoints.ResourceCountainer(
	word = messages.StringField(1),
)

@endpoints.api('hangmanEndPoints', version='1')
class hangmanEndPoints(remote.service):

    @endpoints.method()
    def letterGiven():
        pass

    @endpoints.method()
    def wordGiven():
    	pass
print 'Content-type: text/plain'
print ''
print 'Hello there Chuck'
