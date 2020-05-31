<template>
  <div id="main" class="container">
    <div class="fixed-top">
      <nav class="navbar navbar-dark" style="background-color:#553C7B">
        <img src="../assets/earbudclubimage.png" height="80px;" />
      </nav>
    </div>

    <FlashMessage></FlashMessage>

    <h1>hello</h1>
    <VueBootstrapTypeahead
      :data="songs"
      v-model="songSearch"
      size="lg"
      :serializer="songSerializer"
      placeholder="Search songs or artists"
      @hit="selectedSong = $event"
    >
      <!-- Begin custom suggestion slot -->
      <template slot="suggestion" slot-scope="{ data, htmlText }">
        <div class="d-flex align-items-center">
          <img class="rounded-circle" :src="data.album_art" style="width: 40px; height: 40px;" />

          <!-- Note: the v-html binding is used, as htmlText contains
          the suggestion text highlighted with <strong> tags-->
          <span class="ml-4" v-html="htmlText"></span>
          <i class="ml-auto fab fa-github-square fa-2x"></i>
        </div>
      </template>
    </VueBootstrapTypeahead>
    <button type="button" class="btn btn-primary col-sm-12" v-on:click="queueSong">QUEUE THIS SONG</button>
  </div>
</template>


<script>
const TYPEAHEAD_URL =
  `https://` + process.env.API_HOST + `/tracks?service=:service&q=:q`;
const PLAYER_URL = `https://` + process.env.API_HOST + `/player/`;
import _ from "underscore";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";
import * as VueCookie from "vue-cookie";

export default {
  name: "SongSelect",
  components: {
    VueBootstrapTypeahead
  },
  props: {
    service: String,
    roomCode: String
  },
  data() {
    return {
      songs: [],
      songSearch: "",
      selectedSong: null,
      isConnected: false,
      socketMessage: ""
    };
  },
  sockets: {
    connect() {
      // Fired when the socket connects.
      this.isConnected = true;
    },

    disconnect() {
      this.isConnected = false;
    },

    // Fired when the server sends something on the "messageChannel" channel.
    messageChannel(data) {
      this.socketMessage = data;
    }
  },
  methods: {
    pingServer() {
      // Send the "pingServer" event to the server.
      this.$socket.emit("pingServer", "PING!");
    },
    getService: function() {
      let result = VueCookie.get("SERVICE");
      if (result) {
        return result;
      } else {
        this.$emit("deleteCookies");
      }
    },
    getRoomCode: function() {
      let result = VueCookie.get("ROOM_CODE");
      if (result) {
        return result;
      } else {
        this.$emit("deleteCookies");
      }
    },
    queueSong: function() {
      let url = PLAYER_URL;
      let that = this;
      return this.$http
        .post(url, {
          service: that.getService(),
          uri: that.selectedSong.uri,
          room_code: that.getRoomCode()
        })
        .then(function(response) {
          console.log(response);
          that.songSearch = ""; // clear input
          that.$socket
            .to(that.getRoomCode())
            .emit("song queued", { selected_song: that.selectedSong });
          that.flashMessage.success({
            title: "Hooray!",
            message: "Your song was queued."
          });
        })
        .catch(function(error) {
          console.log(error);
          that.$emit("deleteCookies");
          location.reload();
        });
    },
    songSerializer: function(song) {
      return `${song.name} - ${song.artists.join(", ")}`;
    },
    getSongs: function(query) {
      //const res = await fetch(
      //  API_URL.replace(":q", query).replace(":service", this.service)
      //);
      let url = TYPEAHEAD_URL.replace(":q", query).replace(
        ":service",
        this.getService()
      );
      let that = this;
      return this.$http
        .get(url)
        .then(function(response) {
          console.log(response);
          that.songs = response.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  watch: {
    songSearch: _.debounce(function(query) {
      if (query) {
        this.getSongs(query);
      }
    }, 500),

    socketMessage: function(message) {
      this.flashMessage.success({
        title: "Someone just added...",
        message: message.selected_song
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Permanent+Marker&display=swap");
h1 {
  color: #ffffff;
}
button {
  font-family: "Luckiest Guy", cursive;
  font-size: xx-large;
}
a {
  font-family: "Arial", sans-serif;
}
button,
button:hover,
button:visited,
button:active {
  margin-top: 20px;
  font-family: "Luckiest Guy", cursive;
  font-size: xx-large;

  background-color: #553c7b;
  color: #ffffff;
  border: 0 solid;
  border-radius: 12px;
  box-shadow: none;
}
</style>
