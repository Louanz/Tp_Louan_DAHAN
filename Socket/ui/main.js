import { io } from "./node_modules/socket.io-client/dist/socket.io.esm.min.js";


const socket = io("http://localhost:3000")


socket.on("connect", () => {
  console.log(`🚩socket id is ${socket.id}`); 
});

socket.on("disconnect", () => {
  console.log(`🚩socket has been disconnected`); // undefined
});

socket.on("sport", (args) => {
    console.log(`sport => data ${args}`)
})

