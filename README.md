# Hangman endpoints
Endpoints for a hangman game.

## Installation
 - 1 Download zip file or clone the repository

## Setup
Go to wordknik and register for a api key.Assign wordknik key to to the variable ApiKey in Models.py

## To run
 - 1) open command line prompt and navigate to the repo files.
 - 2) type `dev_appserver.py./
 - 3) goto [appspot webpage](https://apis-explorer.appspot.com/apis-explorer)

## Instructions
 When you start the game a string of * will be displayed(numbers and punctuation marks will be visible as well).When you make a guess the used letter array will update to include that letter.If the letter was in the word, it will be placed in that position in the word. If you wrong more than 6 times you lose the game and the game will end.


### How points are rewarded:
 - 0 points are added to your score for losing/quiting
 - 100 points for guessing the word correctly
 - 10 points for each letter guessed correctly
 - an additional 10 points for:
    - guessing correctly that x is in the word
    - guessing correctly that z is in the word 

## Endpoints
- **newGame**
  - method: Get
  - path: new_game
  - parameters: username
  - returns: NewGameForm
  - description: creates a new game

- **userRegister**
  - method: Post
  - path: register_user
  - parameters: name, email
  - returns: SingleMessage
  - description: registers the user in the database

- **CancelGame**
  - method: Post
  - cancel_game/{urlsafeKey}
  - parmeters: urlsafekey
  - returns: NewGameForm
  - description: Quits the game for the user. It does this by turning Games.endgame to true.

- **letterGiven**
  - method: Get
  - path: game_play/{urlsafeKey}
  - parameters: message, letter
  - returns: Response
  - description: Takes user input and verifies it is a letter or not. Then checks to see if it is in the word.

- **get_history**
  - method: Get
  - path: game_history/{urlsafeKey}
  - parameters: name
  - returns: UserGames
  - description: Gets all the users games.

- **get_game**
  - method: Get
  - path: game/{urlsafeKey}
  - parameters:urlsafeKey
  - returns: NewGameForm
  - description: Retrieves a game

- **get_user_score**
  - method:Get
  - path: score/{name}
  - parameters: name
  - returns: UserScores
  - description: Retrieves the current users combined game score

- **get_high_score**
  - method: Get
  - path: score/high_score
  - parameters: none
  - returns: UserScores
  - description: Get a list of the user's highest scoring games

- **get-user_rankings**
  - method: Get
  - path: rankings
  - parameters: None
  - returns: Rankings
  - description: Get a list of user with the highest scores

## Models Include:
  - **User**
    - Stores unique name and (optional) email address.

  - **Game**
    - Stores unique game states. 

  - **Score**
    - Records game data.

## Forms Included:
  - **NewGameForm**
    - urlsafeKey - id of the game
    - userName - name of the user
    - hint - definition of the word
    - word - word user is tring to guess
    - progress - displays the hidden word with parts that were guess correctly revealed

  - **UserScores**
    - items - list of users and their scores
    - message - used to send message to user

  - **Rankings**
    - items - a list of users

  - **Response**
    - response, progress, guess, lettersUsed

  - **SingleMessage**
    - response used for sending messages

  - **UserGames** 
    - items - list of the user's games