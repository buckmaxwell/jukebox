import React from 'react';
import './ServiceSelect.css';


class ServiceSelect extends React.Component {

  render() {
    return (
      <div className="ServiceSelect">
        <h1>Select a premium service to use with your host account</h1>
        <a
          href="/host/spotify-login"
          className="btn btn-primary col-sm-12">
          Spotify
        </a>
      </div >
    );
  }
}

export default ServiceSelect;
