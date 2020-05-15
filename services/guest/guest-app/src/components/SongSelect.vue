<template>
  <div id="main" class="container">
    <h1>hello</h1>
    <VueBootstrapTypeahead
      :data="songs"
      v-model="songSearch"
      size="lg"
      :serializer="songSerializer"
      placeholder="Search songs or artists"
      @hit="selectedSong = $event"
    >
      <template slot="append">
        <button @click="queueSong" class="btn btn-primary">queue this song</button>
      </template>
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
  </div>
</template>


<script>
const TYPEAHEAD_URL = `http://localhost:5001?service=:service&q=:q`;
const PLAYER_URL = "http://localhost:5002";
import _ from "underscore";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";
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
    queueSong: function() {
      let url = PLAYER_URL;
      let that = this;
      return this.$http
        .post(url, {
          service: that.service,
          uri: that.selectedSong.uri,
          room_code: that.roomCode
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
        this.service
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
#main {
  font-family: "Luckiest Guy", cursive;
  font-size: xx-large;
}
a #main {
  font-family: "Arial", cursive;
}
</style>
