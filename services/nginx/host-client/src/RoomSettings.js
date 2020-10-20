import React from 'react';
import './RoomSettings.css';
//import Table from 'react-bootstrap/Table'
//import MaterialTable from "material-table";
import DataTable from 'react-data-table-component';
import axios from 'axios';
import { Button } from 'react-bootstrap'
import FollowRoomModal from './FollowRoomModal';

const roomTableColumns = [
  {
    name: 'Room Code',
    selector: 'code',
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
    selector: 'expiration_human',
    sortable: true,
    right: true,
  },
];

class RoomSettings extends React.Component {
  constructor(props) {
    super(props);
    this.getRoomTableData = this.getRoomTableData.bind(this);
    this.addRoom = this.addRoom.bind(this);
    this.handleRoomClicked = this.handleRoomClicked.bind(this);
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

  handleRoomClicked(room_row) {
    console.log(room_row)
  }

  componentDidMount() {
    this.setState({ isLoading: true });
    this.getRoomTableData();
  }


  render() {
    return (
      <section className="RoomSettings">
        <h1>Rooms you host or follow</h1>
        <div className="mb-5">
          <Button
            className="btn btn-secondary"
            onClick={this.addRoom}
          >
            Add Room
          </Button>
          <FollowRoomModal />
        </div>
        <DataTable
          title=""
          highlightOnHover={true}
          striped={false}
          columns={roomTableColumns}
          data={this.state.roomTableData}
          onRowClicked={this.handleRoomClicked}
        />
      </section>
    );
  }
}

export default RoomSettings;