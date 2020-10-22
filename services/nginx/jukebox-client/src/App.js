import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Connection from "./Connection";
import NavBar from "./NavBar";
import RoomCodeForm from "./RoomCodeForm";
import SongSelect from "./SongSelect";
import Flash from "./Flash";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleRoomJoined = this.handleRoomJoined.bind(this);
    this.handleLeaveRoom = this.handleLeaveRoom.bind(this);
    this.setFlashMessage = this.setFlashMessage.bind(this);
    this.state = { roomCode: null, flashMessage: null, flashAlbumArt: null };
  };

  handleRoomJoined(roomCode) {
    this.setState({ roomCode });
  }

  handleLeaveRoom() {
    this.setState({ roomCode: null });
  }

  saveStateToLocalStorage() {
    localStorage.setItem('__ebc_song_select__', JSON.stringify(this.state));
  }

  hydrateStateWithLocalStorage() {
    let stringState = localStorage.getItem('__ebc_song_select__') || '{}';
    this.setState(
      JSON.parse(stringState)
    );
  }

  componentDidMount() {
    this.hydrateStateWithLocalStorage();

    // add event listener to save state to localStorage
    // when user leaves/refreshes the page
    window.addEventListener(
      "beforeunload",
      this.saveStateToLocalStorage.bind(this)
    );
  }

  componentWillUnmount() {
    window.removeEventListener(
      "beforeunload",
      this.saveStateToLocalStorage.bind(this)
    );

    // saves if component has a chance to unmount
    this.saveStateToLocalStorage();
  }

  setFlashMessage(flashMessage, flashAlbumArt) {
    this.setState({ flashMessage, flashAlbumArt });
  }

  render() {
    const isLoggedIn = this.state.roomCode;
    let body;
    if (isLoggedIn) {
      body = <SongSelect className="SongSelect"
        onLeaveRoom={this.handleLeaveRoom}
        roomCode={this.state.roomCode}
        setFlashMessage={this.setFlashMessage}
      />;
    } else {
      body = <RoomCodeForm className="RoomCodeForm" onRoomJoined={this.handleRoomJoined} onLeaveRoom={this.handleLeaveRoom} />;
    }

    return (
      <div className="App">
        <NavBar />
        <Connection checked={isLoggedIn ? "checked" : ""} />
        <main className="container">
          {body}
          <Flash message={this.state.flashMessage} art={this.state.flashAlbumArt} />
        </main>
      </div>
    );
  }
}

export default App;
