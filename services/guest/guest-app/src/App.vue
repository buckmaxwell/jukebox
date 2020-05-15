<template>
  <div id="app">
    <RoomCodeForm
      @setRoomCode="setRoomCode($event)"
      @setLoggedIn="setLoggedIn($event)"
      :room-code="roomCode"
      :logged-in="loggedIn"
      v-if="!loggedIn"
    />
  </div>
</template>

<script>
import RoomCodeForm from "./components/RoomCodeForm.vue";

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
    setLoggedIn: function(value) {
      alert("am ghere");
      this.loggedIn = value;
    },
    setRoomCode: function(value) {
      this.roomCode = value;
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
