import React from 'react';
import axios from 'axios';

class RoomCodeForm extends React.Component {
  // do we need a constructor here?
  constructor(props) {
    super(props);
    this.state = { value: '' };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(e) {
    let that = this;
    axios.get(process.env.REACT_APP_API_HOST + "/host/room/" + this.state.value)
      .then(function (response) {
        that.props.onRoomJoined(response.data.room_code);
      })
      .catch(function (error) {
        console.log(error);
        that.props.onLeaveRoom();
      });
    e.preventDefault();
  }

  render() {
    return (
      <section className="RoomCodeForm">
        <h1>Room Code</h1>
        <article className="article-bubble bubble-large">
          <p>Get the code from a friend or follow a public room.</p>
          <form onSubmit={this.handleSubmit} className="text-center">
            <input
              maxLength="4"
              type="text"
              value={this.state.value}
              className="form-control col-sm-12 jb-input"
              placeholder="Enter 4 Character Code"
              onChange={this.handleChange}
            />
            <input type="submit" className="btn btn-primary" value="Join Room" />
          </form>
        </article>
      </section>
    );
  }
}

export default RoomCodeForm;
