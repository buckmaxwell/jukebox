import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import NavBar from "./NavBar";
import RoomCodeForm from "./RoomCodeForm";
import SongSelect from "./SongSelect";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleRoomJoined = this.handleRoomJoined.bind(this);
    this.handleLeaveRoom = this.handleLeaveRoom.bind(this);
    this.state = { roomCode: null, service: null };
  };

  handleRoomJoined(roomCode, service) {
    this.setState({ roomCode, service });
  }

  handleLeaveRoom() {
    this.setState({ roomCode: null, service: null });
  }

  render() {
    const isLoggedIn = this.state.roomCode && this.state.service;
    let body;
    if (isLoggedIn) {
      body = <SongSelect onLeaveRoom={this.handleLeaveRoom} service={this.state.service} roomCode={this.state.roomCode} />;
    } else {
      body = <RoomCodeForm onRoomJoined={this.handleRoomJoined} onLeaveRoom={this.handleLeaveRoom} />;
    }

    return (
      <div className="App">
        <NavBar onLeaveRoom={this.handleLeaveRoom} />
        <div className="container">
          {body}
        </div>
      </div>
    );
  }
}

export default App;
