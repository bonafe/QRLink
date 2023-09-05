//import Quagga from './quagga.js'; // ES6

export class WebcamViewer {
    constructor(videoElement) {
      this.videoElement = videoElement;
      this.iniciar(videoElement);
    }

    iniciar(videoElement){
        Quagga.init({
            inputStream : {
              name : "Live",
              type : "LiveStream",
              target: videoElement
            },
            decoder : {
              readers : ["code_128_reader"]
            }
          }, function(err) {
              if (err) {
                  console.log(err);
                  return
              }
              console.log("Initialization finished. Ready to start");
              Quagga.start();
          });
    }
  
    async start() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.videoElement.srcObject = stream;
      } catch (error) {
        console.error("Erro ao acessar a webcam:", error);
      }
    }
  
    stop() {
      const stream = this.videoElement.srcObject;
      const tracks = stream.getTracks();
  
      tracks.forEach((track) => {
        track.stop();
      });
  
      this.videoElement.srcObject = null;
    }
  }
  
  
  