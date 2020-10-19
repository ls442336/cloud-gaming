// get DOM elements
var dataChannelLog = document.getElementById('data-channel'),
    iceConnectionLog = document.getElementById('ice-connection-state'),
    iceGatheringLog = document.getElementById('ice-gathering-state'),
    signalingLog = document.getElementById('signaling-state'),
    btn_answer = document.getElementById("btn_answer"),
    btn_send = document.getElementById("btn_send"),
    canvas = document.getElementById("canvas"),
    ping = document.getElementById("ping");


var ctx = canvas.getContext("2d");
var img = null
var img_loading = new Image();
var isLoading = false;
var next = true;
var isPinging = false;

img_loading.onload = function() {
    img = img_loading
    isLoading = false;
}

function draw() {
    ctx.clearRect(0, 0, 640, 480);
    
    if(img != null) {
        ctx.drawImage(img, 0, 0, 640, 480)
    }
}

setInterval(draw, 16)

// peer connection
var pc = null;
var answer = null;

// data channel
var dc = null, dcInterval = null;

var id = -1;

var msgs = 0
var time = ''
var firstFrame = false

function createPeerConnection() {
    var config = {
        sdpSemantics: 'unified-plan'
    };
 

    config.iceServers = [{urls: ['stun:stun.1.google.com:19302']}];

    pc = new RTCPeerConnection(config);

    // register some listeners to help debugging
    pc.addEventListener('icegatheringstatechange', function () {
        console.log(' -> ' + pc.iceGatheringState);
    }, false);
    
    //iceGatheringLog.textContent = pc.iceGatheringState;

    pc.addEventListener('iceconnectionstatechange', function () {
       console.log(' -> ' + pc.iceConnectionState);
    }, false);
    //iceConnectionLog.textContent = pc.iceConnectionState;

    pc.addEventListener('signalingstatechange', function () {
        console.log(' -> ' + pc.signalingState);
    }, false);
    // signalingLog.textContent = pc.signalingState;

    return pc;
}

function negotiate() {
    return pc.createOffer().then(function (offer) {
        return pc.setLocalDescription(offer);
    }).then(function () {
        // wait for ICE gathering to complete
        return new Promise(function (resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function () {
        var offer = pc.localDescription;

        offer = JSON.stringify({
            sdp: offer.sdp,
            type: offer.type
        })

        console.log(offer)
    }).catch(function (e) {
        alert(e);
    });
}

function setAnswer() {
	answer = JSON.parse(answer)

    pc.setRemoteDescription(answer).then((e) => {
      console.log(e)  
    }).catch((e) => {
        console.log(e)
    })
}

function start() {
    pc = createPeerConnection();

    var data_channel = pc.createDataChannel('data', {ordered: false});

    data_channel.onopen = function() {
        data_channel.send(JSON.stringify({
            action: 'openned'
        }))

        setInterval(function(){
            if(next){
                data_channel.send(JSON.stringify({
                    action: 'next'
                }))

                next = false;
                isPinging = true;
            } else {
                data_channel.send(JSON.stringify({
                    action: 'ping'
                }))
            }
        }, 16)

        setInterval(function() {
            data_channel.send(JSON.stringify({
                action: 'get_ping',
                start: (new Date).getTime()
            }))
        }, 5000);
    }

    data_channel.onmessage = function(evt) {
        // msgs++;
        // document.title = msgs;

        try{ 
        let data = JSON.parse(evt.data)

        if(data['action'] == "frame") {
            next = true;
            isPinging = false;
            firstFrame = true;

            try{
                if(isLoading == false) {
                    let data = JSON.parse(evt.data)
                    img_loading.src = data.frame
                    isLoading = true
                }
            }catch(e){
            }
        } else if(data['action'] == 'wait') {
            next = true;
            isPinging = false;
        } else if(data['action'] == 'pong') {
            if(!firstFrame) {
                next = true
                isPinging = false;
            }
        } else if(data['action'] == 'get_ping') {
            ping.innerText = (((new Date()).getTime()) - parseFloat(data['start'])) + ' ms';
        } else if(data['action'] == 'frame_error') {
            next = true;
            isPinging = false
        }
    }catch(e) {
        if(isPinging) {
            next = true;
        }
    }
    }

    negotiate();
}