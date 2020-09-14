import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

function RoomPicker() {
  
  const history = useHistory();

  const [roomId, setRoomId] = useState("");

  function handleChange(event) {
    setRoomId(event.target.value);
  }

  async function handleCreate() {
    // Send CreateRoom API then load canvas with the room ID
    await fetch("http://127.0.0.1:8080/create/" + roomId);
    return handleJoin();
  }

  function handleJoin() {
    // Load canvas with the room ID
    history.push("/join/" + roomId);
  }

  return (
    <div>
      <label>
        Room ID:
        <input type="text" value={roomId} onChange={handleChange} />
      </label>
      <button onClick={handleCreate}>Create</button>
      <button onClick={handleJoin}>Join</button>
    </div>
  );
}

export default RoomPicker;