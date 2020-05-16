<template>
  <div id="main" class="container">
    <div class="fixed-top">
      <nav class="navbar navbar-dark" style="background-color:#553C7B">
        <h1>
          <svg
            class="bi bi-speaker"
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M9 4a1 1 0 11-2 0 1 1 0 012 0zm-2.5 6.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z" />
            <path
              fill-rule="evenodd"
              d="M4 0a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V2a2 2 0 00-2-2H4zm6 4a2 2 0 11-4 0 2 2 0 014 0zM8 7a3.5 3.5 0 100 7 3.5 3.5 0 000-7z"
              clip-rule="evenodd"
            />
          </svg>
        </h1>
        <img src="../assets/earbudclubimage.png" height="80px;" />
        <h1>
          <svg
            class="bi bi-speaker"
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M9 4a1 1 0 11-2 0 1 1 0 012 0zm-2.5 6.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z" />
            <path
              fill-rule="evenodd"
              d="M4 0a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V2a2 2 0 00-2-2H4zm6 4a2 2 0 11-4 0 2 2 0 014 0zM8 7a3.5 3.5 0 100 7 3.5 3.5 0 000-7z"
              clip-rule="evenodd"
            />
          </svg>
        </h1>
      </nav>
    </div>

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
const TYPEAHEAD_URL = `http://${process.env.API_HOST}/tracks?service=:service&q=:q`;
const PLAYER_URL = `http://${process.env.API_HOST}/player`;
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
      selectedSong: null
    };
  },
  methods: {
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
        })
        .catch(function(error) {
          console.log(error);
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
          console.log("error");
          console.log(error);
          console.log("error");
          that.$emit("deleteCookies");
        });
    }
  },
  watch: {
    songSearch: _.debounce(function(query) {
      if (query) {
        this.getSongs(query);
      }
    }, 500)
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
