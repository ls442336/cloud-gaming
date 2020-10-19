const createPeerConnection = () => {
  var config = {
    sdpSemantics: "unified-plan"
  };

  config.iceServers = [
    { urls: ["stun:stun.1.google.com:19302"] },
    {
      urls: ["turns:3.231.220.194:3478"],
      username: "trabalhofinal",
      credential: "trabalhofinal"
    }
  ];

  let pc = new RTCPeerConnection(config);

  pc.addEventListener(
    "icegatheringstatechange",
    function() {
      console.log(" -> " + pc.iceGatheringState);
    },
    false
  );

  pc.addEventListener(
    "iceconnectionstatechange",
    function() {
      console.log(" -> " + pc.iceConnectionState);
    },
    false
  );

  pc.addEventListener(
    "signalingstatechange",
    function() {
      console.log(" -> " + pc.signalingState);
    },
    false
  );

  return pc;
};

const Status = {
  NONE: "NONE",
  CONNECTING_TO_SERVER: "CONNECTING_TO_SERVER",
  SERVER_CONNECTION_ERROR: "SERVER_CONNECTION_ERROR",
  WAITING_REGISTER: "WAITING_REGISTER",
  REQUESTING_SESSION: "REQUESTING_SESSION",
  SEARCHING_INSTANCE: "SEARCHING_INSTANCE",
  NO_INSTANCES_AVAILABLE: "NO_INSTANCES_AVAILABLE",
  INSTANCE_FOUND: "INSTANCE_FOUND",
  WAITING_ANSWER: "WAITING_ANSWER",
  WAITING_GAME_DOWNLOAD: "WAITING_GAME_DOWNLOAD",
  DOWNLOADING_GAME: "DOWNLOADING_GAME",
  OPENNING_GAME: "OPENNING_GAME",
  WAITING_FRAMES: "WAITING_FRAMES",
  STREAMING: "STREAMING",
  SESSION_ENDED: "SESSION_ENDED"
};

const Translation = {
  NONE: "NONE",
  CONNECTING_TO_SERVER: "Estabelecendo comunicação com o servidor",
  SERVER_CONNECTION_ERROR: "Falha ao se conectar ao servidor",
  WAITING_REGISTER: "Aguardando confirmação de registro",
  REQUESTING_SESSION: "Iniciando sessão",
  SEARCHING_INSTANCE: "Procurando instâncias disponíveis",
  NO_INSTANCES_AVAILABLE: "Nenhuma instância disponível no momento",
  INSTANCE_FOUND: "Instância encontrada",
  WAITING_ANSWER: "Estabelecendo comunicação com a instância",
  WAITING_GAME_DOWNLOAD: "Aguardando instância iniciar o download do jogo",
  DOWNLOADING_GAME: "Baixando o jogo na instância",
  OPENNING_GAME: "Abrindo o jogo",
  WAITING_FRAMES: "Aguardando imagens",
  STREAMING: "STREAMING",
  SESSION_ENDED: "SESSION_ENDED"
};

const KEY_MAP = {
  a: false,
  b: false,
  c: false,
  d: false,
  e: false,
  f: false,
  g: false,
  h: false,
  i: false,
  j: false,
  k: false,
  l: false,
  m: false,
  n: false,
  o: false,
  p: false,
  q: false,
  r: false,
  s: false,
  t: false,
  u: false,
  v: false,
  w: false,
  x: false,
  y: false,
  z: false,
  13: "{ENTER}",
  37: "{LEFT}",
  39: "{RIGHT}",
  40: "{DOWN}",
  38: "{UP}",
  8: "{BACKSPACE}",
  27: "{ESC}",
  9: "{TAB}",
  32: "{SPACE}"
};

const keysPressed = {};

class GspClient {
  constructor(gameId, streamRenderer, gspClientInfoId, gspInfoScreen) {
    this.id = null;
    this.pc = null;
    this.conn = null;
    this.status = Status.NONE;
    this.streamRenderer = streamRenderer;
    this.dataChannel = null;
    this.inputChannel = null;
    this.numOfDataReceived = 0;
    this.isImageDataLoading = false;
    this.selectedGame = gameId;
    this.hasFramesBeenReceived = false;
    this.gspClientInfo = document.getElementById(gspClientInfoId);
    this.gspInfoScreen = document.getElementById(gspInfoScreen);

    this.events = [];
    this.lastTimeMove = new Date().getTime();

    var self = this;

    window.onkeydown = evt => {
      let keyCode = evt.keyCode;

      if (String.fromCharCode(keyCode).toLowerCase() in KEY_MAP) {
        self.events.push({
          type: "key_down",
          key: String.fromCharCode(keyCode).toLowerCase(),
          time: new Date().getTime(),
          pressed: true
        });
      } else if (keyCode in KEY_MAP) {
        self.events.push({
          type: "key_down",
          key: KEY_MAP[keyCode],
          time: new Date().getTime()
        });
      }
    };

    window.onkeyup = evt => {
      // let keyCode = evt.keyCode;
      // if (String.fromCharCode(keyCode).toLowerCase() in KEY_MAP) {
      //   self.events.push({
      //     type: "key_up",
      //     key: String.fromCharCode(keyCode).toLowerCase(),
      //     time: new Date().getTime()
      //   });
      // } else if (keyCode in KEY_MAP) {
      //   self.events.push({
      //     type: "key_up",
      //     key: KEY_MAP[keyCode],
      //     time: new Date().getTime()
      //   });
      // }
    };

    window.onmousedown = evt => {
      // self.events.push({
      //   type: "mouse_down",
      //   time: new Date().getTime()
      // });
    };

    window.onmouseup = evt => {
      // self.events.push({
      //   type: "mouse_up",
      //   time: new Date().getTime()
      // });
    };

    window.onmousemove = evt => {
      // if (new Date().getTime() - self.lastTimeMove < 33) {
      //   return;
      // }
      // self.lastTimeMove = new Date().getTime();
      // let x =
      //   (evt.clientX - self.streamRenderer.canvas.offsetLeft) /
      //   self.streamRenderer.canvas.width;
      // let y =
      //   (evt.clientY - self.streamRenderer.canvas.offsetTop) /
      //   self.streamRenderer.canvas.height;
      // if (x >= 0 && x <= 1 && y >= 0 && y <= 1) {
      //   self.events.push({
      //     type: "mouse_move",
      //     x: x,
      //     y: y,
      //     time: new Date().getTime()
      //   });
      // }
    };

    this.changeStatus(Status.CONNECTING_TO_SERVER);
  }

  connect = (host, port) => {
    this.conn = new WebSocket(`ws://${host}:${port}`);

    var self = this;

    this.conn.onopen = () => {
      self.status = self.changeStatus(Status.WAITING_REGISTER);

      // Tenta se registrar
      self.conn.send(
        JSON.stringify({
          route: "register_user"
        })
      );
    };

    this.conn.onerror = err => {
      self.changeStatus(Status.SERVER_CONNECTION_ERROR);
    };

    this.conn.onmessage = msg => {
      try {
        const data = JSON.parse(msg.data);

        switch (data.type) {
          case "status":
            self.handleStatus(data);
            break;
          case "action":
            self.handleAction(data);
            break;
        }
      } catch {}
    };
  };

  handleStatus = payload => {
    switch (payload.status) {
      case "register_success":
        this.changeStatus(Status.REQUESTING_SESSION);
        this.id = payload.user;

        // Pede para iniciar sessão
        this.conn.send(
          JSON.stringify({
            route: "users/start_session",
            user: this.id,
            game: this.selectedGame
          })
        );
        break;
      case "searching_instance":
        this.changeStatus(Status.SEARCHING_INSTANCE);
        break;
      case "no_instances_available":
        this.changeStatus(Status.NO_INSTANCES_AVAILABLE);
        break;
      case "instance_found":
        this.changeStatus(Status.INSTANCE_FOUND);
        break;
      case "downloading_game":
        this.changeStatus(Status.DOWNLOADING_GAME);
        break;
      case "openning_game":
        this.changeStatus(Status.OPENNING_GAME);
        break;
      case "streaming":
        this.changeStatus(Status.WAITING_FRAMES);
        this.gspInfoScreen.style.display = "none";
        break;
      case "session_ended":
        this.changeStatus(Status.SESSION_ENDED);
        break;
    }
  };

  handleAction = payload => {
    switch (payload.action) {
      case "get_offer":
        this.pc = createPeerConnection();

        var self = this;

        // Data channel
        this.dataChannel = this.pc.createDataChannel("data", {
          ordered: false,
          maxRetransmits: 500
        });

        this.dataChannel.onopen = function() {
          self.dataChannel.send(
            JSON.stringify({
              timestamp: new Date().getTime()
            })
          );
        };

        this.dataChannel.onmessage = function(evt) {
          self.numOfDataReceived++;
          // document.title = self.numOfDataReceived;

          let data = evt.data;

          // Pega informações do pacote
          let info_size = new DataView(data.slice(-4)).getInt32(0);
          let data_size = data.byteLength;

          let info = JSON.parse(
            new TextDecoder().decode(
              data.slice(data_size - info_size - 4, data_size - 4)
            )
          );

          let image_data = data.slice(0, data_size - info_size - 4);

          // Calcula o ping
          document.title =
            "Ping: " + (new Date().getTime() - info.timestamp) + " ms";

          if (
            !self.isLoadingImageData &&
            !self.streamRenderer.isImageLoading &&
            info.has_frame
          ) {
            let imageArrayBuffer = image_data;
            let imageBytes = new Uint8Array(imageArrayBuffer);
            let imageBlob = new Blob([imageBytes.buffer]);

            // Carregar imagem
            let fileReader = new FileReader();

            fileReader.onload = evt => {
              const imageData = evt.target.result;
              self.streamRenderer.loadFrame(imageData);
              self.isImageDataLoading = false;
              self.hasFramesBeenReceived = true;
            };
            fileReader.onerror = evt => {
              self.isImageDataLoading = false;
            };
            fileReader.readAsDataURL(imageBlob);

            self.isImageDataLoading = true;
          }

          self.dataChannel.send(
            JSON.stringify({
              timestamp: new Date().getTime()
            })
          );
        };

        // Input channel
        this.inputChannel = this.pc.createDataChannel("input", {
          ordered: false,
          maxRetransmits: 500
        });

        this.inputChannel.onopen = function() {
          self.events = [];
          self.inputChannel.send(
            JSON.stringify({
              events: []
            })
          );
        };

        this.inputChannel.onmessage = function(evt) {
          if (self.hasFramesBeenReceived) {
            const events = [...self.events];
            self.events = [];
            self.inputChannel.send(
              JSON.stringify({
                events: events
              })
            );
          } else {
            self.events = [];
            self.inputChannel.send(
              JSON.stringify({
                events: []
              })
            );
          }
        };

        this.negotiate(payload);
        break;
      case "answer":
        this.pc
          .setRemoteDescription(payload.answer)
          .then(e => {
            console.log(e);
          })
          .catch(e => {
            console.log(e);
          });

        this.conn.send(
          JSON.stringify({
            route: "users/answer_received",
            session_id: payload.session_id
          })
        );

        this.changeStatus(Status.WAITING_GAME_DOWNLOAD);
        break;
    }
  };

  negotiate = payload => {
    var self = this;
    let pc = this.pc;

    return pc
      .createOffer()
      .then(function(offer) {
        return pc.setLocalDescription(offer);
      })
      .then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
          if (pc.iceGatheringState === "complete") {
            resolve();
          } else {
            function checkState() {
              if (pc.iceGatheringState === "complete") {
                pc.removeEventListener("icegatheringstatechange", checkState);
                resolve();
              }
            }
            pc.addEventListener("icegatheringstatechange", checkState);
          }
        });
      })
      .then(function() {
        var offer = pc.localDescription;

        self.conn.send(
          JSON.stringify({
            route: "users/get_answer",
            session_id: payload.session_id,
            offer: {
              sdp: offer.sdp,
              type: offer.type
            }
          })
        );

        self.changeStatus(Status.WAITING_ANSWER);
      })
      .catch(function(e) {
        //TODO: Tratar possíveis erros
      });
  };

  changeStatus = status => {
    console.log(this.status + " => " + status);
    this.gspClientInfo.innerText = Translation[status];
    this.status = status;
  };
}

export default GspClient;
