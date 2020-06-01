const express = require('express')
const cors = require('cors');
const app = express()

// origin not allowed allow all
app.use(cors());

//set the template engine ejs
app.set('view engine', 'ejs')

//middlewares
app.use(express.static('public'))


//routes
app.get('/', (req, res) => {
  res.render('index')
})

//Listen on port 3000
server = app.listen(8081, '0.0.0.0')


//socket.io instantiation
const io = require("socket.io")(server)

//listen on every connection
io.on('connection', (socket) => {
  console.log('New user connected')

  //default username
  socket.username = "Anonymous"

  socket.on('join_room', function (data) {
    console.log('joining room...')
    socket.join(data.room_code);
    console.log('joined room')
  });

  //listen on new_message
  socket.on('song_queued', (data) => {
    //broadcast the new message
    //io.sockets.emit('new_message', { song: data.song, username: socket.username });

    io.sockets.to(data.room_code).emit('song_queued', { song: data.song, username: socket.username })
  })

  //listen on change_username
  socket.on('change_username', (data) => {
    socket.username = data.username
  })


  //listen on typing
  socket.on('typing', (data) => {
    socket.broadcast.emit('typing', { username: socket.username })
  })
})