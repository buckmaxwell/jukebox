<template>
  <div class="container">
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

    <form class="roomCodeForm form-inline">
      <div class="form-group col-sm-12">
        <label for="roomCode">ROOM CODE</label>
        <input
          maxlength="5"
          type="text"
          class="form-control col-sm-12"
          id="roomCode"
          aria-describedby="roomCodeHelp"
          placeholder="ENTER 5 LETTER CODE"
        />
        <br />
        <button type="submit" class="btn btn-primary col-sm-12">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "RoomCodeForm",
  props: {
    msg: String
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
