import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import logo from './assets/logo.png'; // Tell webpack this JS file uses this image
import './NavBar.css';


class NavBar extends React.Component {

  render() {
    return (
      <header className="NavBar">
        <Navbar className="container" collapseOnSelect expand="lg" variant="dark" sticky="top">
          <Navbar.Brand href="/">
            <img src={logo} width="200px;" alt="Logo" />
          </Navbar.Brand>
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ml-auto" activeKey="/">
              <Nav.Link href="/">Queue Songs</Nav.Link>
              <Nav.Link href="/rooms">Host or Cohost</Nav.Link>
              <Nav.Link href="/about/">About</Nav.Link>
            </Nav>
          </Navbar.Collapse>
          <Nav.Link className="btn btn-secondary ml-auto btn-create-room" href="/">
            Create room
          </Nav.Link>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        </Navbar>
      </header>
    );
  }
}

export default NavBar;
