// CANVAS
const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

// TODO(hyunbumy): Re-adjust the board size once the initial board state is returned by the server.
canvas.height = 500;
canvas.width = 500;

// variable for initial board state
var boardInitial;

// Socket.io
// TODO(hyunbumy): Use a separate config file to specify the endpoint address.
var socket = io('http://34.94.112.136:8080/canvas')
socket.on('connect', function () {
	console.log(socket.id);
});

socket.on('initialize-board', function (board) {
	// turn JSON into imageData
	let initialBoard = JSON.parse(board);
	let initialImagedata = new ImageData(
		new Uint8ClampedArray(initialBoard.data),
		initialBoard.width,
		initialBoard.height);
	ctx.putImageData(initialImagedata, 0, 0);
});

socket.on('broadcast-stroke', function (stroke) {
	let updatedBoard = updateBoard(stroke.diffs);
	console.log(updatedBoard);
	ctx.putImageData(updatedBoard, 0, 0);
});

function updateBoard(diffs) {
	let currentBoard = ctx.getImageData(0, 0, canvas.width, canvas.height);
	for (let i = 0; i < diffs.length; i++) {
		let diff = diffs[i];
		currentBoard.data[diff.coord] = diff.val;
	}
	return currentBoard;
}

// get difference btw initial & after board
function getDiffs(board_i, board_a) {
	let diffs = [];
	for (let i = 0; i < board_a.data.length; i++) {
		if (board_i.data[i] != board_a.data[i]) {
			diffs.push({ "coord": i, "val": board_a.data[i] });
		}
	}
	console.log(diffs);
	return diffs;
}

// detecting drawing action
let painting = false;
function startPos(e) {
	boardInitial = ctx.getImageData(0, 0, canvas.width, canvas.height);
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
	const boardAfter = ctx.getImageData(0, 0, canvas.width, canvas.height);
	console.log(boardAfter);
	// get difference & emit
	socket.emit('send-stroke', {diffs: getDiffs(boardInitial, boardAfter)});
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

canvas.addEventListener("touchstart", function(e){
    var touch = e.touches[0];
    var mouseEvent = new MouseEvent("mousedown", {
      clientX: touch.clientX,
	  clientY: touch.clientY
	});
	canvas.dispatchEvent(mouseEvent);
	e.preventDefault();
});
canvas.addEventListener("touchend", function(e) {
	let touch = e.touches[0];
    let mouseEvent = new MouseEvent("mouseup");
	canvas.dispatchEvent(mouseEvent);
	e.preventDefault();
});
canvas.addEventListener("touchmove", function(e) {
	let touch = e.touches[0];
    let mouseEvent = new MouseEvent("mousemove", {
      clientX: touch.clientX,
	  clientY: touch.clientY
	});
	canvas.dispatchEvent(mouseEvent);
	e.preventDefault();
});
