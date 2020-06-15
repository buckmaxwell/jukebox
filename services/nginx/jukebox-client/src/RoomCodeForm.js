import React from 'react';
import axios from 'axios';
import './RoomCodeForm.css';

class RoomCodeForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };
  };

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(e) {
    let that = this;
    axios.get(process.env.REACT_APP_API_HOST + "/host/room/" + this.state.value)
      .then(function (response) {
        that.props.onRoomJoined(that.state.value);
      })
      .catch(function (error) {
        console.log(error);
        that.props.onLeaveRoom();
      });
    e.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className="roomCodeForm form-inline">
        <div className="form-group col-sm-12">
          <label>ROOM CODE</label>
          <input
            maxLength="4"
            type="text"
            value={this.state.value}
            className="form-control col-sm-12 jb-input"
            placeholder="ENTER 4 CHARACTER CODE"
            onChange={this.handleChange}
          />
          <input type="submit" className="btn btn-primary col-sm-12" value="JOIN ROOM" />
        </div>
      </form>
    );
  }
}

export default RoomCodeForm;
