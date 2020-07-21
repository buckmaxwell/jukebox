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
        <Button className="btn btn-primary col-sm-12" variant="primary" onClick={this.handleShow}>
          Follow Room
      </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Follow a room</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form onSubmit={this.handleSubmit}>
              <Form.Group controlId="formRoomCode">
                <Form.Label>Room Code</Form.Label>
                <Form.Control type="text" placeholder="ENTER 4 CHARACTER CODE" onChange={this.handleChange} />
                <Form.Text className="text-muted">
                  Get this from a friend or follow a public room
              </Form.Text>
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
            </Button>
            </Form>
          </Modal.Body>
        </Modal>
      </>
    );
  }
}

export default FollowRoomModal;