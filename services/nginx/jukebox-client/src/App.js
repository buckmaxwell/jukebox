import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import NavBar from "./NavBar";
import RoomCodeForm from "./RoomCodeForm";

//import SongSelect from "./SongSelect";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleRoomJoined = this.handleRoomJoined.bind(this);
    this.handleLeaveRoom = this.handleLeaveRoom.bind(this);
    this.state = { roomCode: null };
  };

  handleRoomJoined(roomCode) {
    this.setState({ roomCode });
  }

  handleLeaveRoom() {
    this.setState({ roomCode: null });
  }

  render() {
    //const isLoggedIn = this.state.roomCode;
    let body;
    //if (isLoggedIn) {
    //  body = <SongSelect onLeaveRoom={this.handleLeaveRoom} />;
    //} else {
    //  body = <RoomCodeForm onRoomCodeSubmit={this.handleRoomCodeSubmission} />;
    //}
    body = <RoomCodeForm onRoomJoined={this.handleRoomJoined} />;

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
