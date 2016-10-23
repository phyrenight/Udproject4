import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint
import random
import string
from models import Game, User, Score
from models import NewGameForm, UsersGames, UserScores, Letters
from models import Rankings, RankingForm
import hashlib
from utils import get_by_urlsafe

VOIDMESSAGE = endpoints.ResourceContainer(
    message_types.VoidMessage)

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
    @endpoints.method(REQUEST_LETTER, Response, path="game_play/{urlsafeKey}", http_method="POST", name="make_guess")
    def letterGiven(self, request):
        """
            checks to see if user's guess is in the word.
        """
        game_data = get_by_urlsafe(request.urlsafeKey, Game)
        if game_data.endGame == False:
            if request.letter is None:
                response ="Nothing entered. Please enter a letter." 
                return Response(response=response)
            else:   
                letter = "{}".format(request.letter)
                if len(letter) > 1 or letter.isalpha() is False:
                   return Response(response="Please enter a letter")
                else: 
                    if letter in game_data.lettersUsed:
                        n = game_data.lettersUsed[0]
                        message = '{} has already been used'.format(letter)
                    else:
                        message = hitOrMissLetter(letter, game_data)
                    return Response(response=message, progress=game_data.progress,
                               lettersUsed=game_data.lettersUsed)# Letters(items=[i.get_letter() for i in game.lettersUsed]))
        else:
            message = "Game has already ended"
            return Response(response=message, progress=game_data.progress,
                             lettersUsed=game_data.lettersUsed)
        
# new_game
    @endpoints.method(REQUEST_NEW_GAME,  NewGameForm, path="/new_game", http_method="GET", name="new_game")
    def newGame(self, request):
        """ 
            args: choice - contains the users guessed letter
            creates a new game
            returns: user - urlsafekey based off of the users key
                     hint - definitin of the word
                     word - a randomly generated word
                     progress - astericks string that is as long as the word
        """
        game = Game()
        user = User.query(User.name == request.user_name).get()
        if not user:
            return game.get_form(message="That user does not exist")
        else:
            game = Game.new_game(user.key)
            return game.get_form(message="Good luck!") #"Good luck")

    @endpoints.method(REGISTER_USER, SingleMessage,
                      path='register_User',
                      http_method="POST",
                      name='register_User')
    def UserRegister(self, request):
        """
            register a new user.
            returns SingleMessage - message stating whether registration was successful.
        """
        if request.name == None or request.email == None:
            return SingleMessage(response="No user name/email entered.")
        print request.name
        user = User.query().fetch()
        if user:
            for i in user:
                print i
                if request.name == i.name:
                    print i
                    return SingleMessage(response="User name already in use.")
                elif request.email == i.email:
                    return SingleMessage(response="Email address already in use.")
        
        newUser = User()
        newUser.name = request.name
        newUser.email = request.email
        newUser.put()
        return SingleMessage(response="New user registered")
                     #NewGameForm
    @endpoints.method(REQUEST_GAME, SingleMessage, path='cancel_game/{urlsafeKey}', http_method="POST",
                     name='cancel_game')
    def CancelGame(self, request):
        """
           Cancels one of the user's game.
        """
        game = get_by_urlsafe(request.urlsafeKey, Game)
        if game == 'Invalid Key':
           return SingleMessage(response=game)
        else:
            if game.endGame:
                return SingleMessage(response='game already ended.')
            else: 
                end_Game(game, won=False)
                return SingleMessage(response="Game cancelled.")
        

    @endpoints.method(REQUEST_WORD, UsersGames, path='game_history/{name}', name='user_history', http_method="GET")
    def get_history(self,request):
        """
           gets the user's game history.
        """
        user = User.query(User.name == request.name).get()
        if user == None:
            #raise endpoints.NotFoundException("User can not be found.")
            game = Game()
            game.get_form(message ="User can not be found")
            return UsersGames(items=game)
        else:
            games = Game.query(Game.user == user.key)
            return UsersGames(items=[i.get_form() for i in games]) # Game.query(Game.user == user.key)])

    @endpoints.method(REQUEST_GAME, NewGameForm, path='game/{urlsafeKey}', http_method='GET', name='game')
    def get_game(self, request):
        """
            gets a single game
        """
        game = get_by_urlsafe(request.urlsafeKey, Game)
        if game == 'Invalid Key':
            game = Game()
            return game.get_form(message="Game not found.")
        else:
            return game.get_form(message="game retrieved.")

    @endpoints.method(REQUEST_WORD, UserScores, path='score/{name}', http_method='GET', name='user_score')
    def get_user_score(self, request):
        """
            gets a list of the user's scores
        """
        score = Score.query(Score.player == request.name).fetch()
        if len(score) == 0:
            return UserScores(message = "No scores were found for this user.")
        else:
            return UserScores(items=[i.get_form() for i in score])
        
    @endpoints.method(VOIDMESSAGE, UserScores, path='/score/High_scores',
                      http_method="Get", name="high_score")
    def get_high_score(self, request):
        """
            get a list of the users with the highest scores.
            returns: UserScores - message class
        """
        try:
            highScore = Score.query().fetch()
            return UserScores(items=[i.get_form() for i in highScore])
        except:
            return UserScores(message = "No high scores to return")

    @endpoints.method(VOIDMESSAGE, Rankings, path='/rankings',
                      http_method='Get', name="rankings")
    def get_user_rankings(self, request):
        """
            gets a list of users and their score/ranking
        """
        items = []
        users = User.query().fetch()
        for i in users:
            usersGames = Score.query(Score.player == i.name).fetch()
            finishedGames = len(usersGames)
            for n in usersGames:
                totalScore =+ n.score
            percent = totalScore/finishedGames
            items.append(RankingForm(player=i.name,
                                       finishedGames=finishedGames,
                                       totalScore=totalScore,
                                       percent=percent))
            return Rankings(items=items)

def hitOrMissLetter(letter, game):
    """
       args: letter- user's letter guess
            game - current game.
       checks to see if the word contains the guesses letter.
       returns: a message if you passsed or failed.
    """
    maxGuess = 6
    guess = game.lettersUsed
    if game.lettersUsed is None:
        game.lettersUsed = [] 
    game.lettersUsed.append(letter) # place holder till letterUsed can be changed to a ListProperty 
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
            end_Game(game, won=True)  # new
            return "You have guessed the word. {}".format(game.word)
        else:
            game.put()
            return "{} was found in the word".format(letter)

    else:
        game.guesses += 1
        if game.guesses == maxGuess:
            return "You have failed to guess this word."
        else:
            return "{} is not in the word. ".format(letter)


def end_Game(game, won):
    """
        args: game - 
              won -
        ends the user's game.
    """
    game.endGame = True
    game.put()
    user = User.query(User.key == game.user).get()
    gameScore = get_Score(game, won)
    score = Score(player=user.name, score=gameScore,won=won)
    score.put()

def get_Score(game, won):
    """
        args: game - 
              won -
        calculates the score for the user's game.
        returns: finalScore - the final score of the game. 
    """
    finalScore = 0 
    value = 10
    if won == True:
        finalScore += 100
        finalScore += (len(game.word) * value)
    else:
        lettersGuessedCorrect = 0
        for i in game.progress:
            if i != '*':
                lettersGuessedCorrect += 1
                finalScore += ((len(game.word - lettersGuessedCorrect)) * value)
    if 'x' in game.progress:
        finalScore += value
    if 'z' in game.progress:
        finalScore += value
    return finalScore

APPLICATION = endpoints.api_server([hangmanApi])
