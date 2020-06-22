// CANVAS
const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

// TODO(hyunbumy): Re-adjust the board size once the initial board state is returned by the server.
canvas.height = 500;
canvas.width = 500;

// Socket.io
var socket = io('http://localhost:8080')
socket.on('connect', function () {
	console.log(socket.id);
});

socket.on('broadcast-board', function (imagedata) {
	console.log(imagedata);
	ctx.putImageData(imageData, 0, 0);
});

// detecting drawing action
let painting = false;
let stroke = [];
function startPos(e) {
	painting = true;
	// fix not drawing when clicking
	draw(e);
}
function endPos() {
	painting = false;
	// reset path every time when ending
	// fixes lines being all connected
	ctx.beginPath();

	// send info using websocket
	const snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
	console.log(snapshot);
	socket.emit('send-stroke', snapshot);
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
