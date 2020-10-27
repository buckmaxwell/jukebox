import React from 'react';
import { Button } from 'react-bootstrap'

class ServiceSelect extends React.Component {

  render() {
    return (
      <section className="ServiceSelect">
        <h1>Connect your host account</h1>
        <article className="article-bubble">
          <p>Please select a premium service to use with your host account.</p>
          <Button
            href="/spotify/login"
            className="btn btn-primary">
            Spotify
          </Button>
        </article>
      </section>
    );
  }
}

export default ServiceSelect;
