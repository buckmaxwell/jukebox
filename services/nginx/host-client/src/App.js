import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { createBrowserHistory } from 'history';
import NavBar from "./NavBar";
import ServiceSelect from "./ServiceSelect";
import RoomSettings from "./RoomSettings";

// TODO: is this necessary, what does it do
export const history = createBrowserHistory({
  basename: process.env.PUBLIC_URL
});

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { userId: null, service: null };
  };

  saveStateToLocalStorage() {
    localStorage.setItem('__ebc_room_settings__', JSON.stringify(this.state));
  }

  hydrateStateWithLocalStorage() {
    let stringState = localStorage.getItem('__ebc_room_settings__') || '{}';
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

  render() {
    const isLoggedIn = this.state.userId && this.state.service;
    let body;
    if (isLoggedIn) {
      body = <RoomSettings className="RoomSettings"
        service={this.state.service}
        userId={this.state.userId}
      />;
    } else {
      body = <ServiceSelect className="ServiceSelect" />;
    }

    return (
      <div className="App">
        <NavBar />
        <div className="container">
          {body}
        </div>
      </div>
    );
  }
}

export default App;
