<template>
  <div id="main">
    <VueBootstrapTypeahead
      :data="songs"
      v-model="addressSearch"
      size="lg"
      :serializer="s => s.text"
      placeholder="Type an address..."
      @hit="selectedAddress = $event"
    />
  </div>
</template>

<script>
const API_URL = `http://localhost:5001?service=${this.service}&q=:q`;
import _ from "underscore";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";
export default {
  name: "SongSelect",
  data() {
    return {
      service: "",
      songs: [],
      songSearch: "",
      roomCode: null,
      selectedSong: null
    };
  },
  methods: {
    async getSongs(query) {
      const res = await fetch(API_URL.replace(":q", query));
      const suggestions = await res.json();
      this.songs = suggestions.suggestions;
    }
  },
  watch: {
    songSearch: _.debounce(function(addr) {
      this.getSongs(addr);
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
input,
label {
  font-family: "Luckiest Guy", cursive;
  font-size: xx-large;
}
input {
  padding: 20px 12px;
  background-color: #e0e0e0;
  color: #000;
  border: 0 solid;
  border-radius: 12px;
  box-shadow: none;
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
.roomCodeForm {
  margin-top: 150px;
}
</style>
