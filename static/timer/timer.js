
const testlauf = false;          // <<-- HIER UMSCHALTEN. Optionen sind "true" und "false".


// ============================ Ab hier bitte nichts änderen ====================

const S = 1000;
const M = S*60;

// diffs are in ms
const diff10min = 10*M;   // 10 minutes
var diff60s = 30*S;     // 60 seconds
if (testlauf){ diff60s = 3*S; } // bei testlauf 60sek durch 3sek ersetzen

const updateInterval = 50; // in milliseconds

var previousdiff = undefined;

// State functions
var STATE = 0; // see below for states 0,1,2
var setState = function(s){
  var prev = STATE;
  STATE = s;
  log(["State:", prev,"->",s]);
}
var inState=function(state,f){ if (STATE === state){f();} }

/* Timer:
State:
0 means Paused
1 means Counting
2 means Blinking

start Clock:  0 -> Space -> 1
pause Clock:  1 -> Space -> 0
stop blinking: 2 -> Space -> (0 and reset to previous deadline)
start blinking: 1 -> countFinish -> 2
ready 10min:    (any state) -> Press 1 -> (0 and set timer to 10min)
ready 60sec:    (any state) -> Press 9 -> (0 and set timer to 60sec)
*/

var timeinterval = undefined;

var timeRemaining = undefined; // in milliseconds

var log = function(s){console.log(s.join(" "))}

var updateClock = function(){
  log(["Should not be: Null updateClock called"]);
}

function setClockBorderColor(classname){
  var clockBorder = document.querySelector("#clockborder");
  clockBorder.setAttribute("class",classname);
}
 
function initializeClock(diff) {
  log(["Init Clock: ",diff]);
  timeRemaining = diff;
  previousdiff = diff;
  var clock = document.getElementById('clockdiv');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  updateClock = function(updateInterval2) {
    log(["updateClock:",updateInterval2])
    var f = function(){
      timeRemaining = timeRemaining - updateInterval2;
      if (timeRemaining > 0){
        var seconds = Math.floor(timeRemaining/1000)%60;
        var minutes = Math.floor(Math.floor(timeRemaining/1000)/60)%60;
        minutesSpan.innerHTML = ('0' + minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + seconds).slice(-2);
      }
      else {
        setState(2);
        minutesSpan.innerHTML = "00";
        secondsSpan.innerHTML = "00";
        clearInterval(timeinterval);
        startBlinking()
      }
    };
    inState(1,f);
    inState(0,f);
  }
  updateClock(0);
}

function startClock(){
  timeinterval = setInterval(function(){updateClock(updateInterval);}, updateInterval);
  setClockBorderColor("counting");
  setState(1);
}

function pauseClock(){
  clearInterval(timeinterval);
  setClockBorderColor("paused");
  setState(0);
}

var blinktimer = undefined;
var c=undefined;
var updateBlink = function(){
  if (c) {
    setClockBorderColor("blink1");
  }
  else {
    setClockBorderColor("blink2");
  }
  c = (!c);
}

function startBlinking(){
  blinktimer=setInterval(updateBlink,700);
  setClockBorderColor("blink2");
  c=true;
}

function stopBlinking(reinitializeClock){
  clearInterval(blinktimer);
  setClockBorderColor("paused");
  setState(0);
  if(reinitializeClock) { initializeClock(previousdiff); };
}

function keypress(e) {
  switch (e.key){
    case " ":
      log(["Got space."]);
      switch (STATE) {
        case 0:
          startClock()
          break;
        case 1:
          pauseClock()
          break;
        case 2:
          stopBlinking(true)
          break;
      }
      break;
    case "1":
      log(["Got 1."]);
      switch (STATE) {
        case 1:
          pauseClock()
          break;
        case 2:
          stopBlinking(false)
          break;
      }
      initializeClock(diff10min);
      break;
    case "6":
      log(["Got 6."]);
      switch (STATE) {
        case 1:
          pauseClock()
          break;
        case 2:
          stopBlinking(false)
          break;
      }
      initializeClock(diff60s);
      break;
    default: 
      // do nothing
      break;
  }
}


window.addEventListener("keypress", keypress, false);

window.addEventListener("load", function(e){setState(0);initializeClock(diff10min);}, false);
