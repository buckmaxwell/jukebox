<template>
  <div id="app">
    <RoomCodeForm
      @setRoomCode="setRoomCode($event)"
      @setLoggedIn="setLoggedIn($event)"
      :room-code="roomCode"
      :logged-in="loggedIn"
      v-if="isLoggedIn() == false"
    />
  </div>
</template>

<script>
import RoomCodeForm from "./components/RoomCodeForm.vue";
import * as VueCookie from "vue-cookie";

export default {
  name: "App",
  components: {
    RoomCodeForm
  },
  data() {
    return {
      loggedIn: false,
      roomCode: ""
    };
  },
  methods: {
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
