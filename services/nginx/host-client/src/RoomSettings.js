import React from 'react';
import './RoomSettings.css';
//import Table from 'react-bootstrap/Table'
import ReactDOM from "react-dom";
import MaterialTable from "material-table";


class RoomSettings extends React.Component {

  render() {

    return (
      <div className="RoomSettings">
        <h1>RoomSettings Component</h1>
        <div style={{ maxWidth: '100%' }}>
          <MaterialTable
            title="Your Rooms"
            columns={[
              { title: 'Code', field: 'name' },
              { title: 'Role', field: 'surname' },
              { title: 'Expiration', field: 'birthYear', type: 'numeric' },
            ]}
            data={[
              { name: 'Mehmet', surname: 'Baran', birthYear: 1987, birthCity: 63 },
              { name: 'Zerya Betül', surname: 'Baran', birthYear: 2017, birthCity: 34 },
            ]}
            actions={[
              {
                icon: 'delete',
                tooltip: 'Delete Room',
                onClick: (event, rowData) => confirm("You want to delete " + rowData.name)
              },
              {
                icon: 'save_alt',
                tooltip: 'Export as playlist',
                onClick: (event, rowData) => confirm("You want to delete " + rowData.name)
              },
            ]}
          />
        </div>
      </div >
    );
  }
}

export default RoomSettings;