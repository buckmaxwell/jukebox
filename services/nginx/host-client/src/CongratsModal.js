import React from 'react';
import { Modal, Button } from 'react-bootstrap'

class CongratsModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = { show: true };

    this.handleClose = this.handleClose.bind(this);
  }

  handleClose() {
    this.setState({ show: false });
  }

  render() {
    return (
      <Modal
        show={this.state.show}
        onHide={this.handleClose}
        animation={false}
        centered
        className="text-center modal-large"
      >
        <Modal.Header closeButton />
        <Modal.Body>
          <h2>Congrats!</h2>
          <p>You just added a new room, here is how you can start listening to songs:</p>
          <ol>
            <li>Make sure your Spotify account is connected</li>
            <li>Queue songs to be played</li>
            <li>Share the room code with your friends</li>
          </ol>
          <Button className="btn btn-primary" onClick={this.handleClose}>
            Done
          </Button>
        </Modal.Body>
      </Modal>
    );
  }
}

export default CongratsModal;