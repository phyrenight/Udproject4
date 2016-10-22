function newGame() {
	console.log("ppppp");
  //  game = gapi.client.hangmanEndPoints.userRegister('Marc', "preston9@comcast.net");
	console.log(game);
	console.log("lol");
}
function highscore() {
}

function init() {
  console.log("hello");
  console.log(window.location.host)
  gapi.client.load('hangmanEndPoints','v1', newGame, window.location.host)
  console.log("llllll")
  gapi.client.hangmanEndPoints.userRegister('Marc');
}