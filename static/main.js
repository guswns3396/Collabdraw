// CANVAS
const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

// Socket.io
var socket = io('http://localhost:8080')
socket.on('connect', function() {
	console.log(socket.id);
});

socket.on('receive-update', function(data) {
	console.log(data);
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
	console.log(stroke);
	socket.emit('send-stroke', stroke);
	
	// reset stroke
	stroke = [];
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
	stroke.push([e.clientX, e.clientY]);
}
canvas.addEventListener("mousedown", startPos);
canvas.addEventListener("mouseup", endPos);
canvas.addEventListener("mousemove", draw);
