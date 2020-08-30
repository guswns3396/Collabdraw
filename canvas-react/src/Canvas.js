import React, { useRef, useState } from 'react';

function Canvas() {
  const [isPainting, setIsPainting] = useState(false);
  const [boardSnapshot, setBoardSnapshot] = useState(null);
  const canvasRef = useRef(null);
 
  return (
    <canvas
      ref={canvasRef}
      width={window.innerWidth}
      height={window.innerHeight}
      onMouseUp={
        e => {
          setIsPainting(false);
          
          const canvas = canvasRef.current;
          const ctx = getContext(canvas);

          ctx.beginPath();
          const boardAfter = getCurrentBoard(canvas);
          console.log(boardAfter);
          // Send the board diff over Socket.IO
        }
      }
      onMouseDown={
        e => {
          const canvas = canvasRef.current;
          setBoardSnapshot(getCurrentBoard(canvas));
          setIsPainting(true);
          draw(e, canvas);
        }
      }
      onMouseMove={
        e => {
          if (isPainting) {
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

export default Canvas;