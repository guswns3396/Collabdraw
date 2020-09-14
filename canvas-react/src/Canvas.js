import React, { useRef, useState, useLayoutEffect } from 'react';
import { useParams } from 'react-router-dom';
import socketIOClient from 'socket.io-client';

const socket = socketIOClient("http://127.0.0.1:8080/canvas");

function Canvas() {
  const { roomId } = useParams();

  const isPainting = useRef(false);
  const boardSnapshot = useRef(null);
  const canvasRef = useRef(null);
  
  const [canvasWidth, setCanvasWidth] = useState(100);
  const [canvasHeight, setCanvasHeight] = useState(100);

  useLayoutEffect(() => {
    socket.emit("join", { room_id: roomId });

    socket.on("invalid-room", msg => {
      throw new Error(msg);
    });

    socket.on("initialize-board", payload => {
      const initialBoard = payload["board"];
      const initialImagedata = new ImageData(
        new Uint8ClampedArray(initialBoard.data),
        initialBoard.width,
        initialBoard.height
      );

      setCanvasWidth(initialBoard.width);
      setCanvasHeight(initialBoard.height);
      getContext(canvasRef.current).putImageData(initialImagedata, 0, 0);
    });

    socket.on("broadcast-stroke", payload => {
      updateBoard(canvasRef.current, payload["diffs"]);
    });
  });

  return (
    <canvas
      style={{border: "1px solid black"}}
      ref={canvasRef}
      width={canvasWidth}
      height={canvasHeight}
      onMouseUp={
        e => {
          isPainting.current = false;

          const canvas = canvasRef.current;
          const ctx = getContext(canvas);

          ctx.beginPath();
          const boardAfter = getCurrentBoard(canvas);
          console.log(boardAfter);
          socket.emit("send-stroke", {
            diffs: getDiffs(boardSnapshot.current, boardAfter),
            room_id: roomId
          });
        }
      }
      onMouseDown={
        e => {
          const canvas = canvasRef.current;
          boardSnapshot.current = getCurrentBoard(canvas);
          isPainting.current = true;
          draw(e, canvas);
        }
      }
      onMouseMove={
        e => {
          if (isPainting.current) {
            draw(e, canvasRef.current);
          }
        }
      }
    />
  );
}

function getContext(canvas) {
  return canvas.getContext('2d');
}

function getCurrentBoard(canvas) {
  return getContext(canvas).getImageData(0, 0, canvas.width, canvas.height);
}

function draw(e, canvas) {
  const ctx = getContext(canvas);

  ctx.lineWidth = 10;
  ctx.lineCap = "round";
  ctx.lineTo(e.clientX, e.clientY);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.clientX, e.clientY)
}

function updateBoard(canvas, diffs) {
  const ctx = getContext(canvas);
  const newBoard = ctx.getImageData(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < diffs.length; i++) {
    const diff = diffs[i];
    newBoard.data[diff.coord] = diff.val;
  }
  ctx.putImageData(newBoard, 0, 0);
}

// get difference btw initial & after board
function getDiffs(boardInitial, boardAfter) {
  const diffs = [];
  for (let i = 0; i < boardAfter.data.length; i++) {
    if (boardInitial.data[i] !== boardAfter.data[i]) {
      diffs.push({ "coord": i, "val": boardAfter.data[i] });
    }
  }
  console.log(diffs);
  return diffs;
}

export default Canvas;