import React from 'react';
import './ServiceSelect.css';
import { Jumbotron, Button } from 'react-bootstrap'


class ServiceSelect extends React.Component {

  render() {
    return (
      <div className="ServiceSelect">
        <Jumbotron className="selectJumbo">
          <h1>Select a premium service to use with your host account</h1>
          <hr></hr>
          <p>
            <Button
              href="/host/spotify-login"
              className="btn btn-primary col-sm-12">
              Spotify
            </Button>
          </p>
        </Jumbotron>
      </div >
    );
  }
}

export default ServiceSelect;
