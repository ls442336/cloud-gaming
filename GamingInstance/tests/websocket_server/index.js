const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 9000 });

const test_register = (ws, data) => {
  if (data.route == "gaming_instance/register") {
    ws.send(
      JSON.stringify({
        type: "status",
        status: "register_success",
      })
    );

    ws.send(
      JSON.stringify({
        type: "action",
        action: "start_session",
        session: {
          id: "123",
          game: {
            id: "231123",
            path: "IronSnoutGamejolt/IronSnout.exe",
            bucket_id: "o23oij4321o123",
          },
        },
      })
    );
  }
};

wss.on("connection", function connection(ws) {
  ws.on("message", function incoming(message) {
    data = JSON.parse(message);

    console.log(data);

    test_register(ws, data);
  });
});
