import React from 'react';
import './App.css';

function App() {
  return (
    <canvas
      width={window.innerWidth}
      height={window.innerHeight}
      onClick={event => alert(event.clientX)}
    />
  );
}

export default App;
