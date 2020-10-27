import React from 'react';
import './Connection.css';

const Connecion = ({ checked }) => {
  return (
    <div className="container Connection">
      <input type='checkbox' name="spotify-connection" checked={checked} disabled />
      <label htmlFor="spotify-connection">Spotify</label>
    </div>
  )
}

export default Connecion