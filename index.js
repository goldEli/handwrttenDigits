/*
 * @Author: miaoyu
 * @Date: 2020-06-15 15:42:10
 * @LastEditTime: 2020-06-15 23:08:12
 * @LastEditors: miaoyu
 * @Description:
 */
// import { saveAs } from 'file-saver';

var canvas = document.querySelector("#myCanvas");
var reBtn = document.querySelector("#jsReBtn")
var clearBtn = document.querySelector("#jsClearBtn")
var showNum = document.querySelector("#showNum")

var ctx = canvas.getContext("2d");

var mouse = { x: 0, y: 0 };
var last_mouse = { x: 0, y: 0 };

/* Mouse Capturing Work */
canvas.addEventListener(
  "mousemove",
  function (e) {
    last_mouse.x = mouse.x;
    last_mouse.y = mouse.y;

    mouse.x = e.pageX - this.offsetLeft;
    mouse.y = e.pageY - this.offsetTop;
  },
  false
);
handleClear();

/* Drawing on Paint App */
ctx.lineWidth = 10;
ctx.lineJoin = "round";
ctx.lineCap = "round";
ctx.strokeStyle = "rgb(255,255,255)";

canvas.addEventListener(
  "mousedown",
  function (e) {
    canvas.addEventListener("mousemove", onPaint, false);
  },
  false
);

canvas.addEventListener(
  "mouseup",
  function () {
    canvas.removeEventListener("mousemove", onPaint, false);
    // window.location = canvas.toDataURL("image/png");
  },
  false
);

function onPaint() {
  ctx.beginPath();
  ctx.moveTo(last_mouse.x, last_mouse.y);
  ctx.lineTo(mouse.x, mouse.y);
  ctx.closePath();
  ctx.stroke();
}

function handleRecognize() {
  var c = canvas;
  var d = c.toDataURL("image/png");
  d = d.replace("data:image/png;base64,", "")
  postData('/recognize', { img: d })
  .then(data => {
    console.log(data); // JSON data parsed by `response.json()` call
    showNum.textContent = data.predictions
  });
}

function handleClear() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // draw background
  ctx.fillStyle = "rgb(0,0,0)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}


reBtn.addEventListener("click", handleRecognize)
clearBtn.addEventListener("click", handleClear)

export default {}
