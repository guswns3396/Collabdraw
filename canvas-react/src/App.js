import React from 'react';
import './App.css';
import Canvas from './Canvas';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/">
          <Canvas />
        </Route>
      </Switch>
    </Router>
  )
}

export default App;
