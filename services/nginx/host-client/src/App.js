import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { createBrowserHistory } from 'history';
import Connection from "./Connection";
import NavBar from "./NavBar";
import ServiceSelect from "./ServiceSelect";
import RoomSettings from "./RoomSettings";
import Cookies from 'js-cookie';

// TODO: is this necessary, what does it do
export const history = createBrowserHistory({
  basename: process.env.PUBLIC_URL
});

class App extends React.Component {
  constructor(props) {
    super(props);
    this.setService = this.setService.bind(this);
    this.setUserId = this.setUserId.bind(this);
    this.state = { userId: null, service: null };
  };

  saveStateToLocalStorage() {
    localStorage.setItem('__ebc_room_settings__', JSON.stringify(this.state));
  }

  setService(service) {
    this.setState({ service });
  }

  setUserId(userId) {
    this.setState({ userId });
  }

  hydrateStateWithLocalStorage() {
    let stringState = localStorage.getItem('__ebc_room_settings__') || '{}';
    this.setState(
      JSON.parse(stringState)
    );
  }

  componentDidMount() {
    this.hydrateStateWithLocalStorage();
    let ebc_host_user = Cookies.get('EBC_HOST_USER') || null;
    let ebc_host_auth = Cookies.get('EBC_HOST_AUTH') || null;
    let ebc_host_service = Cookies.get('EBC_HOST_SERVICE') || null;
    this.setState({ userId: ebc_host_user, service: ebc_host_service, authId: ebc_host_auth });

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
        authId={this.state.authId}
      />;
    } else {
      body = <ServiceSelect className="ServiceSelect" thisSetService={this.setService} setUserId={this.setUserId} />;
    }

    return (
      <div className="App">
        <NavBar />
        <Connection checked={isLoggedIn ? "checked" : ""} />
        <main className="container">
          {body}
        </main>
      </div>
    );
  }
}

export default App;
