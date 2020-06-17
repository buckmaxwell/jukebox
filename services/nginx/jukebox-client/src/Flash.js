import React from "react";
import "./Flash.css";
// Refer to https://www.npmjs.com/package/react-flash-message
import FlashMessage from "react-flash-message";

class Flash extends React.Component {
  render() {
    return (
      <div className="container">
        <FlashMessage duration={5000}>
          <div className="flash">

            <img
              className="rounded"
              src={this.props.art}
              style={{
                height: '100px',
                marginRight: '10px',
                width: '100px',
              }}
            />
            <span className="ml-4">{this.props.message}</span>

          </div>
        </FlashMessage>
      </div>
    );
  }
}

export default Flash;