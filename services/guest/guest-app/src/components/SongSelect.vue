<template>
  <div id="main">
    <h1>hello</h1>
    <VueBootstrapTypeahead
      :data="songs"
      v-model="songSearch"
      size="lg"
      :serializer="s => s.name"
      placeholder="Type an address..."
      @hit="selectedAddress = $event"
    />
  </div>
</template>

<script>
const API_URL = `http://localhost:5001?service=:service&q=:q`;
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
    getSongs: function(query) {
      //const res = await fetch(
      //  API_URL.replace(":q", query).replace(":service", this.service)
      //);
      let url = API_URL.replace(":q", query).replace(":service", this.service);
      let that = this;
      return this.$http
        .get(url)
        .then(function(response) {
          console.log(response);
          that.songs = response.data;
        })
        .catch(function(error) {
          console.log(error);
          that.$emit("deleteCookies");
        });
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
