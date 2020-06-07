<template>
<div id="app">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  </head>

  <RoomCodeForm
    @setRoomCode="setRoomCode($event)"
    @setLoggedIn="setLoggedIn($event)"
    @setService="setService($event)"
    @deleteCookies="deleteCookies($event)"
    :room-code="roomCode"
    :logged-in="loggedIn"
    :service="service"
    v-if="isLoggedIn() == false"
  />
  <SongSelect
    @deleteCookies="deleteCookies($event)"
    :service="service"
    :room-code="roomCode"
    v-if="isLoggedIn() == true"
  />
</div>
</template>

<script>
import RoomCodeForm from "./components/RoomCodeForm.vue";
import SongSelect from "./components/SongSelect.vue";
import * as VueCookie from "vue-cookie";

export default {
  name: "App",
  components: {
    RoomCodeForm,
    SongSelect
  },
  data() {
    return {
      loggedIn: false,
      roomCode: "",
      service: ""
    };
  },
  methods: {
    deleteCookies: function() {
      VueCookie.delete("SERVICE");
      VueCookie.delete("ROOM_CODE");
    },
    isLoggedIn: function() {
      if (VueCookie.get("ROOM_CODE")) {
        return true;
      }
      return false;
    },
    setLoggedIn: function(value) {
      this.loggedIn = value;
    },
    setRoomCode: function(value) {
      this.roomCode = value;
      VueCookie.set("ROOM_CODE", value, { expires: "1D" });
    },
    setService: function(value) {
      this.service = value;
      VueCookie.set("SERVICE", value, { expires: "1D" });
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
