// CANVAS
const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

// TODO(hyunbumy): Re-adjust the board size once the initial board state is returned by the server.
canvas.height = 500;
canvas.width = 500;

// variable for initial board state
var board_initial;

// Socket.io
var socket = io('http://localhost:8080/canvas')
socket.on('connect', function () {
	console.log(socket.id);
});

socket.on('broadcast-board', function (imagedata) {
	// turn JSON into imageData
	imagedata = JSON.parse(imagedata);
	array = new Uint8ClampedArray(imagedata.data);
	console.log(imagedata);
	// create new ImageData & update board
	imagedata = new ImageData(array,imagedata.width,imagedata.height);
	ctx.putImageData(imagedata, 0, 0);
});

// detecting drawing action
let painting = false;
function startPos(e) {
	board_initial = ctx.getImageData(0, 0, canvas.width, canvas.height);
	painting = true;
	// fix not drawing when clicking
	draw(e);
}
function endPos() {
	painting = false;
	// reset path every time when ending
	// fixes lines being all connected
	ctx.beginPath();
	// get final board state
	const board_after = ctx.getImageData(0, 0, canvas.width, canvas.height);
	console.log(board_after);
	// get difference btw initial & after board
	let coord = [];
	let val = [];
	for (let i = 0; i < board_after.data.length; i++) {
	    if (board_initial.data[i] != board_after.data[i]) {
	        coord.push(i);
	        val.push(board_after.data[i]);
	    }
	}
	// create JSON
	var diff = {
	    "coord" : coord,
	    "val" : val
	};
    console.log(diff)
	socket.emit('send-stroke', diff);
}
function draw(e) {
	if (!painting) {
		return;
	}
	// draw
	ctx.lineWidth = 10;
	ctx.lineCap = "round";
	ctx.lineTo(e.clientX, e.clientY);
	ctx.stroke();
	ctx.beginPath();
	ctx.moveTo(e.clientX, e.clientY);
}
canvas.addEventListener("mousedown", startPos);
canvas.addEventListener("mouseup", endPos);
canvas.addEventListener("mousemove", draw);
