import React from 'react';
import './ServiceSelect.css';


class ServiceSelect extends React.Component {

  render() {
    return (
      <div className="ServiceSelect">
        <h1>ServiceSelect Component</h1>
        <a href="/host/spotify-login">Authenticate with SPOTIFY</a>
      </div >
    );
  }
}

export default ServiceSelect;
