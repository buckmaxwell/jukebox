import React from 'react';
import './RoomSettings.css';
//import Table from 'react-bootstrap/Table'
//import MaterialTable from "material-table";
import DataTable from 'react-data-table-component';
import axios from 'axios';
import { Button } from 'react-bootstrap'

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

const data = [
  {
    "expires": "just now",
    "id": "DO2W",
    "role": "owner",
    "room_code": "DO2W"
  },
  {
    "expires": "just now",
    "id": "YLJY",
    "role": "owner",
    "room_code": "YLJY"
  },
  {
    "expires": "just now",
    "id": "E919",
    "role": "owner",
    "room_code": "E919"
  },
  {
    "expires": "just now",
    "id": "7M7Z",
    "role": "owner",
    "room_code": "7M7Z"
  }
]

class RoomSettings extends React.Component {
  constructor(props) {
    super(props);
    this.getRoomTableData = this.getRoomTableData.bind(this);
    this.addRoom = this.addRoom.bind(this);
    this.state = { roomTableData: [], isLoading: false };
    this.ROOMS_URL =
      process.env.REACT_APP_API_HOST + "/host/rooms";
  }


  getRoomTableData() {
    let url = this.ROOMS_URL
    let that = this;
    axios.get(url, { withCredentials: true })
      .then(function (response) {
        console.log(response);
        that.setState({ isLoading: false, roomTableData: response.data })
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  addRoom() {
    let url = this.ROOMS_URL
    let that = this;
    axios.post(url, { withCredentials: true })
      .then(function (response) {
        console.log(response);
        that.getRoomTableData();
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  componentDidMount() {
    this.setState({ isLoading: true });
    this.getRoomTableData();
  }


  render() {
    return (
      <div className="RoomSettings">
        <div style={{ maxWidth: '100%' }}>
          <DataTable
            title="Rooms you host or follow"
            columns={roomTableColumns}
            data={this.state.roomTableData}
          />
          <Button
            className="btn btn-primary col-sm-12"
            onClick={this.addRoom}
          >
            Add room
          </Button>

        </div>
      </div >
    );
  }
}

export default RoomSettings;