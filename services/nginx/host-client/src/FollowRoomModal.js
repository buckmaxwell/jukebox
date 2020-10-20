import { Modal, Button, Form } from 'react-bootstrap'
import React from 'react';
import axios from 'axios';


class FollowRoomModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '', show: false };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);

    this.FOLLOWERS_URL =
      process.env.REACT_APP_API_HOST + "/host/rooms/:room_code/followers";
  }

  handleClose() {
    this.setState({ show: false });
  }

  handleShow() {
    this.setState({ show: true });
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    let url = this.FOLLOWERS_URL.replace(":room_code", this.state.value);
    let that = this;
    axios.post(url, { withCredentials: true })
      .then(function (response) {
        console.log(response);
        that.handleClose();
      })
      .catch(function (error) {
        console.log(error);
      });
    //event.preventDefault();
  }

  render() {
    return (
      <>
        <Button className="btn btn-secondary ml-5" onClick={this.handleShow}>
          Follow Room
        </Button>

        <Modal
          show={this.state.show}
          onHide={this.handleClose}
          animation={false}
          centered
          className="text-center modal-large"
        >
          <Modal.Header closeButton />
          <Modal.Body>
            <h2>Follow a room</h2>
            <Form onSubmit={this.handleSubmit}>
              <Form.Group controlId="formRoomCode">
                <Form.Label srOnly>Room Code</Form.Label>
                <p>Get the code from a friend or follow a public room</p>
                <Form.Control type="text" placeholder="Enter 4 Character Code" onChange={this.handleChange} />
              </Form.Group>
              <Button className="btn btn-secondary" type="submit">
                Follow Room
              </Button>
            </Form>
          </Modal.Body>
        </Modal>
      </>
    );
  }
}

export default FollowRoomModal;