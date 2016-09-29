#Hangman endpoints
Endpoints for a hangman game.

##Installation
 - 1 Download zip file or clone the repository

##Setup
Go to wordknik and register for a api key.Assign wordknik key to to the variable ApiKey in Models.py

##To run
 - 1) open command line prompt and navigate to the repo files.
 - 2) type `dev_appserver.py./
 - 3) goto [appspot webpage](https://apis-explorer.appspot.com/apis-explorer)

 ##Instructions
 When you start the game a string of * will be displayed(numbers and punctuation marks will be visible as well).When you make a guess the used letter array will update to include that letter.If the letter was in the word, it will be placed in that position in the word. If you wrong more than 6 times you lose the game and the game will end.


###How points are rewarded:
 - 0 points are added to your score for losing/quiting
 - 100 points for guessing the word correctly
 - 10 points for each letter guessed correctly
 - an additional 10 points for:
    - guessing correctly that x is in the word
    - guessing correctly that z is in the word 

##Endpoints
- **newGame**
  - method: Get
  - path: new_game

- **userRegister**
  - method: Post
  - path: register_user

- **cancelGame**
  - method: Post
  - cancel_game/{urlsafeKey}

- **letterGiven**
  - method: Get
  - path: game_play/{urlsafeKey}

- **getHistory**
  - method: Get
  - path: game_history/{urlsafeKey}

- **getGame**
  - method: Get
  - path: game/{urlsafeKey}

- **get_user_score**
  - method:Get
  - path: score/{name}

- **get_high_score**
  - method: Get
  - path: score/high_score

- **get-user_rankings**
  - method: Get
  - path: rankings