import React from 'react';
import './RoomSettings.css';
//import Table from 'react-bootstrap/Table'
//import MaterialTable from "material-table";
import DataTable from 'react-data-table-component';
import axios from 'axios';
import { ThemeConsumer } from 'styled-components';

const roomTableColumns = [
  {
    name: 'Room Code',
    selector: 'room_code',
    sortable: true,
  },
  {
    name: 'Role',
    selector: 'role',
    sortable: true,
    right: true,
  },
  {
    name: 'Expires',
    selector: 'expires',
    sortable: true,
    right: true,
  },
];

class RoomSettings extends React.Component {
  constructor(props) {
    super(props);
    this.getRoomTableData = this.getRoomTableData.bind(this);
    this.state = { roomTableData: [] };
    this.ROOMS_URL =
      process.env.REACT_APP_API_HOST + "/host/rooms";
  }


  getRoomTableData() {
    let url = this.ROOMS_URL
    let that = this;
    axios.get(url, { withCredentials: true })
      .then(function (response) {
        console.log(response);
        that.setState({ roomTableData: response.data })
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  componentDidMount() {
    this.getRoomTableData();
  }


  render() {
    return (
      <div className="RoomSettings">
        <div style={{ maxWidth: '100%' }}>
          <DataTable
            title="Rooms you host or follow"
            columns={roomTableColumns}
            data={this.roomTableData}
          />
        </div>
      </div >
    );
  }
}

export default RoomSettings;