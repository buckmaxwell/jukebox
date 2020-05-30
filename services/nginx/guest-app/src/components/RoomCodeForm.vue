<template>
  <div class="container">
    <div class="fixed-top">
      <nav class="navbar navbar-dark" style="background-color:#553C7B">
        <img src="../assets/earbudclubimage.png" height="80px;" />
      </nav>
    </div>

    <form class="roomCodeForm form-inline">
      <div class="form-group col-sm-12">
        <label for="roomCode">ROOM CODE</label>
        <input
          maxlength="5"
          type="text"
          class="form-control col-sm-12"
          v-model="roomCode"
          placeholder="ENTER 4 CHARACTER CODE"
        />
        <br />
        <button type="button" class="btn btn-primary col-sm-12" v-on:click="joinRoom">JOIN ROOM</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "RoomCodeForm",
  data() {
    return {
      roomCode: null,
      service: null,
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
    joinRoom: function() {
      let that = this;
      return this.$http
        .get(`https://earbud.club/host/room/` + this.roomCode)
        .then(function(response) {
          console.log(response);

          that.$emit("setLoggedIn", true);
          that.$emit("setRoomCode", response.data.room_code);
          that.$emit("setService", response.data.service);

          that.$socket.emit("join", {
            username:
              Math.random()
                .toString(36)
                .substring(2, 15) +
              Math.random()
                .toString(36)
                .substring(2, 15),
            room: response.data.room_code
          });
        })
        .catch(function(error) {
          console.log(error);
          that.$emit("deleteCookies");
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
