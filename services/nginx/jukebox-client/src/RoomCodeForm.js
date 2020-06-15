import React from 'react';
import './RoomCodeForm.css';

class RoomCodeForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  };

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(e) {
    this.props.onRoomJoined(e.target.value);
    e.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className="roomCodeForm form-inline">
        <div class="form-group col-sm-12">
          <label for="roomCode">ROOM CODE</label>
          <input
            maxLength="4"
            type="text"
            value={this.state.value}
            className="form-control col-sm-12 jb-input"
            placeHolder="ENTER 4 CHARACTER CODE"
            onChange={this.handleChange}
          />
          <input type="submit" className="btn btn-primary col-sm-12" value="JOIN ROOM" />
        </div>
      </form>
    );
  }
}

export default RoomCodeForm;
