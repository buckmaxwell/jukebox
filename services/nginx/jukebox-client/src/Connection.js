import React from 'react';
import './Connection.css';

const Connecion = ({ checked, isLoggedIn, onLeaveRoom }) => {
  return (
    <div className="container Connection">
      <input type='checkbox' name="spotify-connection" checked={checked} disabled />
      <label htmlFor="spotify-connection">Spotify</label>
      {isLoggedIn === true ?
          <button
            className="btn btn-secondary ml-auto"
            onClick={onLeaveRoom}
          >Leave Room</button>
      : null }
    </div>
  )
}

export default Connecion