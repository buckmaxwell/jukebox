import React from 'react';
import axios from 'axios';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
//import 'react-bootstrap-typeahead/css/Typeahead.css';
import './SongSelect.css';

class SongSelect extends React.Component {
  // do we need a constructor here?
  constructor(props) {
    super(props);
    this.handleLeaveRoom = this.handleLeaveRoom.bind(this);
    this.handleGetSongs = this.handleGetSongs.bind(this);
    this.queueSong = this.queueSong.bind(this);
    this.state = { selectedSong: null, isLoading: false, songs: [] };
    //this.songInput = React.createRef();
    this.TYPEAHEAD_URL =
      process.env.REACT_APP_API_HOST + "/tracks?q=:q";
    this.PLAYER_URL = process.env.REACT_APP_API_HOST + "/player/";
  }

  handleLeaveRoom() {
    this.props.onLeaveRoom();
  }

  queueSong() {
    let that = this;
    return axios.post(
      that.PLAYER_URL, {
      spotify_id: that.state.selectedSong.spotify_id,
      isrc: that.state.selectedSong.isrc,
      upc: that.state.selectedSong.upc,
      ean: that.state.selectedSong.ean,
      room_code: that.props.roomCode
    }).then(function (response) {
      console.log(response);
      that.typeahead.clear();
      that.props.setFlashMessage(that.state.selectedSong.name, that.state.selectedSong.album_art)
      window.location.reload(false);
    }).catch(function (error) {
      console.log(error);
      that.props.onLeaveRoom();
    });
  }

  handleGetSongs(query) {
    let url = this.TYPEAHEAD_URL.replace(":q", query);
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
    return (
      <div className="SongSelect">
        <small style={{ "text-align": "right" }} className="small text-muted">Not hearing songs? (1) Make sure spotify is playing (2) go over to Co-Host and follow {this.props.roomCode} if you are not the owner. </small>
        <AsyncTypeahead
          id="song-search-typeahead"
          ref={typeahead => this.typeahead = typeahead}
          className="input-group input-group-lg"
          isLoading={this.state.isLoading}
          labelKey={song => `${song.name} - ${song.artists.join(', ')}`}
          onSearch={this.handleGetSongs}
          onChange={songs => this.setState({ selectedSong: songs[0] })}
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
        <button
          id="qsong"
          type="button"
          className="btn btn-primary col-sm-12"
          onClick={this.queueSong}>
          QUEUE THIS SONG
        </button>
        <div id="flashContainer"></div>
      </div>
    );
  }
}

export default SongSelect;
