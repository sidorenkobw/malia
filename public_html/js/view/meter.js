define(["event-emitter"], function (EventEmitter) {
    class Meter extends EventEmitter {
        constructor(elem) {
            super();

            this.elem = elem;
            this.stream = null;
        }

        setStream(stream) {
            this.stream = stream;

            let ctx = new AudioContext();
            this.analyser = ctx.createAnalyser();

            let microphone = ctx.createMediaStreamSource(stream);
            microphone.connect(this.analyser);

            this.analyser.fftSize = 128;
            this.dataArray = new Uint8Array(this.analyser.fftSize);

            return this;
        }

        start() {
            if (!this.stream) {
                throw new Error("Stream is not set");
            }
            this.update();
            return this;
        }

        update() {
            throw new Error("Not implemented by child class");
        }
    }

    return Meter;
});
