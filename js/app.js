let baseURL = 'http://localhost:6060/';
// let inGame = false;
let form = document.querySelectorAll('form');
let formBtns = document.querySelectorAll('.form_bottuns h1');
let gamesList = document.querySelector('.games_list');
let playersList = document.querySelector('.players_list');
let startMenu = document.querySelector('.startMenu');
let inGame = document.querySelector('.inGame');
let startGameBtn = document.querySelector("#startGame");
let playerId = 0;
let gameId = 0;

let user = {};
form.forEach(x=>{
  x.addEventListener('submit',postMessages, false);
});

formBtns.forEach(x=>{
  x.addEventListener('click',showForm, false);
});

startGameBtn.addEventListener('click',startGame, false);

function showForm(){
  form.forEach(x=>{x.style.display=  "none";});
  document.querySelector("#"+event.srcElement.dataset.show).style.display = "block";
  console.log(event.srcElement.dataset.show);
}

function startGame() {
  _PUT('games/'+gameId+'/players',function(data){
    // console.log("game info");
    // console.log(data);
    if(data.game_character){
      
    }
  });
}

// function checkCookie
// setInterval(checkCookie,5000);

function checkCookie(){
  // console.log(user);
  if(!Object.keys(user).length){
    _GET('sessions/', function(data){
      console.log(data)
      if(data.success != "no data"){
        data = data.success;
        user.name = data.first_name + " " + data.last_name;
        showGameMenu();
      }
    });
  }
}
checkCookie();
function delPlayer(){
  _DEL('players/'+event.srcElement.id);
}
function listenForCharacter(){
  var characterListenSchool = setInterval(function(){
  
    _GET('games/'+gameId+'/players', function(data){
      playersList.innerHTML = "";
      data.forEach(x=>{
        let h2 = document.createElement("h2");
        let h2Text = document.createTextNode(x['player_name']);
        h2.appendChild(h2Text);
        h2.setAttribute("id", x['id']);
        h2.addEventListener('click',delPlayer, false);
        playersList.appendChild(h2);
      });
    });
    
    _GET('players/'+playerId,function(data){
      if(!data[0]){
        location.reload();
      }
      if(data[0].character_title){
        document.querySelector('.character_data').innerHTML= data[0].character_data;
        document.querySelector('.character_title').innerHTML= data[0].character_title;
      }
    });
  
  }, 1000);
}


let updateGameListLoop = setInterval(function(){
  updateGamesList();  
}, 5000);


function killGameListLoop() {
    clearInterval(updateGameListLoop);
}
function killCharacterListenLoop() {
    clearInterval(characterListenSchool);
}

function updateGamesList(){
  gamesList.innerHTML = "";
  games = _GET('games', function(data){
    data.forEach(x=>{
      let h2 = document.createElement("h2");
      let h2Text = document.createTextNode('Game ID: ' + x['game_id']);
      h2.appendChild(h2Text);
      gamesList.appendChild(h2);
    });
  });
}
function _PUT(ext,callback){
  let myInit = {
                method: "PUT",
                credentials: 'include'
               };
  url = baseURL + ext;
  console.log(url)
  fetch(url,myInit).then(function(response) {
      return response.json();
  }).then(function(json) {
    if(callback)callback(json);
  });
}
function _DEL(ext, callback){
  let myInit = {
                method: "DELETE",
                credentials: 'include'
               };
  url = baseURL + ext;
  fetch(url,myInit).then(function(response) {
      return response.json();
  }).then(function(json) {
    if(callback)callback(json);
  });
}

function _GET(ext, callback) {
  url = baseURL + ext;
  fetch(url, {
    method: "GET",
    credentials: 'include'
  }).then(function(response) {
      // console.log(response);
        return response.json();
    }).then(function(json) {
      if(callback)callback(json);
    });
}
function showGameMenu(){
  document.querySelectorAll('.logged_out').forEach(x =>{
    x.style.display = "none";
  });
  document.querySelectorAll('.logged_in').forEach(x =>{
    x.style.display = "block";
  });
  document.querySelector('.games_list').style.display = "block";
  document.querySelector('.logged_in[data-show="players"]').click();
  document.querySelector('#players [name="player_name"]').value = user.name;
  document.querySelector('#games [name="player_name"]').value = user.name;
}
function postMessages(){
  
  event.preventDefault();
  console.log(event);
  url = baseURL + event.srcElement.id;
  thisForm = document.querySelector("#"+event.srcElement.id);
  var formData = new FormData(thisForm);
  let urlEncodedDataPairs = [];

  for (var entry of formData.entries()){
     urlEncodedDataPairs.push(encodeURIComponent(entry[0]) + '=' + encodeURIComponent(entry[1]));
  }
  urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
  
  let myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/x-www-form-urlencoded');
  myHeaders.append('Accept', 'text/html'); 

  let myInit = {
                 method: "POST",
                 headers: myHeaders,
                 body: urlEncodedData,
                 // mode: 'cors',
                 credentials: 'include',
                 // cache: 'default' 
               };
           
  fetch(url, myInit).then(function(response) {
    return response.json();
  }).then(function(data) {
    if(data.error){
      alert(data.error);
    }else{
      if(data.response!="success"){
        if(data.message){
          alert(data.message);
        }else{
          alert("Bad password or email");
        }
      };
      
      if(data.message == "authenticated"){
        console.log("authenticated");
         user.name = data.first_name + " " + data.last_name;
        showGameMenu();
      }
      if(data.message == "created user"){
       console.log("created user");
       user.name = data.first_name + " " + data.last_name;
       console.log(user);
       showGameMenu();
      }
      if(data.message == "joined game"){
        startMenu.style.display = "none";
        inGame.style.display ='block';
        playerId = data.player_id;
        gameId = data.game_id;
        killGameListLoop();
        listenForCharacter();
      }
      if(data.message == "game created"){
        startMenu.style.display = "none";
        inGame.style.display ='block';
        playerId = data.player_id;
        gameId = data.game_id;
        killGameListLoop();
        listenForCharacter();
      }
    }
  });
}
