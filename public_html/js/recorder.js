define(["event-emitter", "view/meter"], function (EventEmitter, Meter) {
    class Recorder extends EventEmitter {
        constructor(successCb, errorCb) {
            super();

            this.mimeType = 'audio/webm;codecs=opus';
            this.chunks = [];
            this.mediaRecorder = null;
            this.meter = null;
            this._isRecording = false;
            this._successCb = successCb;
            this._errorCb = errorCb;

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
                errorCb("Unable to initialize MediaRecorder. Your browser doesn't support MediaRecorder API. Please try using chrome.");
                return;
            }
        }

        setMeter(meter) {
            this.meter = meter;

            // This makes the 'allow page to record?' permission appear.
            navigator.mediaDevices.getUserMedia({"audio": true, "video": false })
                .then((stream) => {
                    this.meter
                        .setStream(stream)
                        .start();

                    this.mediaRecorder = new MediaRecorder(stream, {mimeType: this.mimeType});

                    this.mediaRecorder.ondataavailable = this._onData.bind(this);
                    this.mediaRecorder.onstart = this._onStart.bind(this);
                    this.mediaRecorder.onstop = this._onStop.bind(this);

                    this.mediaRecorder.onerror = (e) => {
                        this.debug(e, "error", "MediaRecorder");
                    };

                    this.mediaRecorder.onwarning = (e) => {
                        this.debug(e, "warning", "MediaRecorder");
                    };

                    if (this._successCb) {
                        this._successCb();
                    }
                }).catch((err) => {
                    // TODO handle this case
                    this.debug("getUserMedia failed", "error", "MediaRecorder");
                    this.debug(err, "error", "MediaRecorder");
                    if (this._errorCb) {
                        this._errorCb("Unable to initialize MediaRecorder. Please make sure to provide permission for recording.", err);
                    }
                });
        }

        startRecording() {
            if (!this.mediaRecorder) {
                return;
            }

            if (this.isRecording()) {
                throw new Error("Recording is in progress");
            }

            this.mediaRecorder.start(/*timeslice*/ 1000);
        }

        stopRecording(callback) {
            if (!this.mediaRecorder) {
                return;
            }

            if (!this.isRecording()) {
                return;
            }

            if (callback) {
                this.once("stop", callback);
            }

            this.mediaRecorder.stop();
        }

        isRecording() {
            return this._isRecording;
        }

        _onStart() {
            this._isRecording = true;
            this.debug('Started, state = ' + this.mediaRecorder.state, "log", "MediaRecorder");
        }

        _onStop() {
            this._isRecording = false;
            this.emit("data-ready", new Blob(this.chunks, {type: this.mimeType}));
            this.chunks = [];
            this.emit("stop");
        }

        _onData(ev) {
            this.chunks.push(ev.data);
            this.debug(`audio recording has ${this.chunks.length} chunks`, "log", "MediaRecorder");
        }
    }

    return Recorder;
});
