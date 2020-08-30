import React, { useRef } from 'react';

function Canvas() {
  const isPainting = useRef(false);
  const boardSnapshot = useRef(null);
  const canvasRef = useRef(null);
 
  return (
    <canvas
      ref={canvasRef}
      width={window.innerWidth}
      height={window.innerHeight}
      onMouseUp={
        e => {
          isPainting.current = false;
          
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

export default Canvas;