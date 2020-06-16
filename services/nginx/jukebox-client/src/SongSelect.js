import React from 'react';
import axios from 'axios';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

import 'react-bootstrap-typeahead/css/Typeahead.css';
import './SongSelect.css';

class SongSelect extends React.Component {
  // do we need a constructor here?
  constructor(props) {
    super(props);
    this.handleLeaveRoom = this.handleLeaveRoom.bind(this);
    this.handleGetSongs = this.handleGetSongs.bind(this);
    this.state = { selectedSong: null, isLoading: false, songs: [] };
    this.TYPEAHEAD_URL =
      process.env.REACT_APP_API_HOST + "/tracks?service=:service&q=:q";
    this.PLAYER_URL = process.env.REACT_APP_API_HOST + "/player/";
  }

  handleLeaveRoom() {
    this.props.onLeaveRoom();
  }

  handleGetSongs(query) {
    let url = this.TYPEAHEAD_URL.replace(":q", query).replace(
      ":service",
      this.props.service
    );
    let that = this;
    axios.get(url)
      .then(function (response) {
        console.log(response);
        that.setState({ songs: response.data })
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    const ref = React.createRef();
    return (
      <AsyncTypeahead
        id="song-search-typeahead"
        ref={ref}
        className="input-group input-group-lg"
        isLoading={this.state.isLoading}
        labelKey={song => `${song.name} - ${song.artists.join(', ')}`}
        onSearch={this.handleGetSongs}
        options={this.state.songs}
        placeholder="Search songs or artists"
        renderMenuItemChildren={(song, props) => (
          <div>
            <img
              className="rounded"
              alt={`${song.name} - ${song.artists.join(', ')}`}
              src={song.album_art}
              style={{
                height: '50px',
                marginRight: '10px',
                width: '50px',
              }}
            />
            <span className="ml-4">{`${song.name} - ${song.artists.join(', ')}`}</span>
          </div>
        )}
        filterBy={(song, props) => {
          /* Song filtering can happen server side only */
          return song
        }}
      />
    );
  }
}

export default SongSelect;
