import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import logo from './assets/logo.png'; // Tell webpack this JS file uses this image
import './NavBar.css';


class NavBar extends React.Component {

  render() {
    return (
      <div className="NavBar">
        <Navbar collapseOnSelect expand="lg" variant="dark" sticky="top">
          <Navbar.Brand href="/">
            <img src={logo} width="200px;" alt="Logo" />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto" activeKey="/">
              <Nav.Link href="/rooms/">Host or Cohost</Nav.Link>
              <Nav.Link
                eventKey="leaveRoom"
                onSelect={this.props.onLeaveRoom}
              >Leave Room</Nav.Link>
              <Nav.Link href="/about/">Trouble Shooting</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div >
    );
  }
}

export default NavBar;
