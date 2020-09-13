import React from 'react';
import './App.css';
import Canvas from './Canvas';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import RoomPicker from './RoomPicker';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/join/:roomId">
          <Canvas />
        </Route>
        <Route path="/">
          <RoomPicker />
        </Route>
      </Switch>
    </Router>
  )
}

export default App;
