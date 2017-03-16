define(["event-emitter", "view/meter"], function (EventEmitter, Meter) {
    class Recorder extends EventEmitter {
        constructor(meterElem, successCb, errorCb) {
            super();

            this.mimeType = 'audio/webm;codecs=opus';
            this.chunks = [];
            this.mediaRecorder = null;
            this._isRecording = false;

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
                errorCb("Unable to initialize MediaRecorder. Your browser doesn't support MediaRecorder API. Please try using chrome.");
                return;
            }

            // This makes the 'allow page to record?' permission appear.
            navigator.mediaDevices.getUserMedia({"audio": true, "video": false })
                .then((stream) => {
                    new Meter(meterElem, stream)
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

                    if (successCb) {
                        successCb();
                    }
                }).catch((err) => {
                // TODO handle this case
                this.debug("getUserMedia failed", "error", "MediaRecorder");
                this.debug(err, "error", "MediaRecorder");
                if (errorCb) {
                    errorCb("Unable to initialize MediaRecorder. Please make sure to provide permission for recording.", err);
                }
            });
        }

        startRecording(word) {
            if (!this.mediaRecorder) {
                return;
            }

            if (this.isRecording()) {
                throw new Error("Recording is in progress");
            }

            this.once("file-ready", ((blob) => {
                this.emit("word-ready", {word: word, blob: blob});
            }));

            this.mediaRecorder.start(/*timeslice*/ 1000);
        }

        stopRecording() {
            if (!this.mediaRecorder) {
                return;
            }

            if (!this.isRecording()) {
                throw new Error("Recorder is not active");
            }

            this.once("data-ready", (function (data) {
                this.emit("file-ready", data);
            }).bind(this));
            this.mediaRecorder.stop();
        }

        cancelRecording(callback) {
            if (!this.mediaRecorder) {
                return;
            }

            this.off("file-ready");

            if (this.isRecording()) {
                if (callback) {
                    this.once("stop", callback);
                }
                this.mediaRecorder.stop();
            }
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
