define([
    "malia",
    "view",
    "recorder",
    "view/meter/speak",
    "bootstrapnotify"
], function (
    malia,
    View,
    Recorder,
    SpeakMeterView,
    BootstrapNotify
) {
    class SpeakView extends View {
        constructor(malia) {
            super();

            this.cfg = malia.cfg || {};

            /* idle|record|edit */
            this.mode = "idle";
            this.isFullscreen = false;
            this.recordTimeout = 15000;
            this.recordTimer = null;

            this.initEls();

            if (malia.debugLog) {
                this.setDebugLog(malia.debugLog);
            }

            if (location.protocol != "https:") {
                var url = location.href.replace(/^http\:/, "https\:");
                this.error('HTTP protocol is not supported. Please open using HTTPS: <a href="'+url+'">'+url+'</a>');
                return;
            }

            this.auth = malia.auth;
            if (!this.auth) {
                this.debug("No auth view", "log", "SpeakView");
                this.error('Internal error: unable to perform authentication.');
                return;
            }

            this.initRecorder();
            this.initEvents();
            this.initButtons();
            this.initKeyboardEvents();
        }

        initRecorder() {
            this.recorder = new Recorder(
                this.render.bind(this),
                this.error.bind(this)
            );

            var meter = new SpeakMeterView($("#wave-graph").get(0));
            meter.on("word-start", function () { console.log("word-start") }.bind(this));
            meter.on("word-stop", function () { console.log("word-stop") }.bind(this));
            this.recorder.setMeter(meter);

            this.recorder.setDebugLog(this.debugLog);
        }

        initEvents() {
            var events = {
                "mode": this.onChangeMode,

                "mode-idle-on":  this.onModeIdleOn,
                "mode-idle-off": this.onModeIdleOff,

                "mode-record-on":  this.onModeRecordOn,
                "mode-record-off": this.onModeRecordOff,

                "fullscreen-on":  this.onFullscreenOn,
                "fullscreen-off": this.onFullscreenOff,

                "word-next":   this.onNextWord
            };

            for (var event in events) {
                this.on(event, events[event].bind(this));
            }
        }

        initEls() {
            this.$app = $("#speakApp");
            this.$textContainer = $("#textContainer");
            this.$btnStartRecording = $("#btnStartRecording");
            this.$btnNext = $("#btnNextWord");
            this.$btnClearText = $("#btnClearText");
        }

        initKeyboardEvents() {
            $(document).on("keydown", this.onKeyPressed.bind(this));
        }

        initButtons() {
            this.$textContainer.on("click", this.onClickNext.bind(this));
            this.$btnStartRecording.click(this.onClickStartRecording.bind(this));
            this.$btnNext.click(this.onClickNext.bind(this));
            this.$btnClearText.click(this.onClickClearText.bind(this));
        }

        onKeyPressed(e) {
            var $target = $(e.target);
            if (e.which == 27) {
                // esc
                if (this.mode != "idle") {
                    this.setMode("idle");
                }
            }
        }

        onClickStartRecording(e) {
            this.setMode(this.mode == "record" ? "idle" : "record");
        }

        onClickNext(e) {
            if (this.mode == "record") {
                this.emit("word-next");
            }
        }

        onClickClearText(e) {
            this.$textContainer.empty();
            this.$btnClearText.prop("disabled", true);
        }

        setMode(mode) {
            var old = this.mode;
            this.mode = mode;
            this.emit("mode", old);
        }

        onChangeMode(old) {
            this.emit("mode-" + old + "-off");
            this.emit("mode-" + this.mode + "-on");
        }

        onModeIdleOn() {
            this.debug("Mode idle on", "log", "SpeakView_ModeChange");
        }

        onModeIdleOff() {
            this.debug("Mode idle off", "log", "SpeakView_ModeChange");
        }

        onModeRecordOn() {
            this.debug("Mode record on", "log", "SpeakView_ModeChange");
            this.setFullscreen(true);
            this.startRecording();

            this.$btnStartRecording.addClass("hidden");
            this.$btnNext.removeClass("hidden");
        }

        onModeRecordOff() {
            this.debug("Mode record off", "log", "SpeakView_ModeChange");
            this.setFullscreen(false);

            this.$btnStartRecording.removeClass("hidden");
            this.$btnNext.addClass("hidden");

            this.stopRecording();
        }

        setFullscreen(flag) {
            this.isFullscreen = !!flag;
            this.emit("fullscreen-" + (this.isFullscreen ? "on" : "off"));
        }

        onFullscreenOn() {
            this.debug("Fullscreen on", "log", "SpeakView");
            this.$app.addClass("fullscreen");
        }

        onFullscreenOff() {
            this.debug("Fullscreen off", "log", "SpeakView");
            this.$app.removeClass("fullscreen");
        }

        onNextWord() {
            this.stopRecording(function () {
                this.startRecording();
            }.bind(this));
        }

        uploadWord(record) {
            this.debug("Upload started", "log", "SpeakView_Upload");

            if (!record) {
                this.showNotification("danger", "Word was not uploaded");
                this.debug("Error: Record is empty", "log", "SpeakView_Upload");
                return;
            }

            this.debug(record, "log", "SpeakView_Upload_Start");

            $.ajax({
                method: "post",
                url: this.cfg.recognizer.url,
                data: record,
                processData: false,
                contentType: false,
            })
                .done(function (data) {
                    this.$btnClearText.prop("disabled", false);
                    if (data.word) {
                        this.$textContainer.append($("<span>").text(data.word));
                        this.$textContainer.append(" ");
                    } else {
                        this.$textContainer.append("...");
                        this.$textContainer.append(" ");
                    }
                    this.scrollToLastWord();
                }.bind(this))
                .fail(function (err) {
                    this.showNotification("danger", "Failed to upload a file. Please check network connection");
                }.bind(this));
        }

        startRecording() {
            this.recorder.startRecording();
            this.debug("Start recording", "log", "SpeakView");

            this.recordTimer = setTimeout((function () {
                this.setMode("idle");
                this.showNotification("danger", "Recording timeout");
            }).bind(this), this.recordTimeout);
        }

        stopRecording(callback) {
            this.recorder.once("data-ready", function (blob) {
                this.uploadWord(blob);
            }.bind(this));

            this.recorder.stopRecording(callback);
            this.debug("Stop recording", "log", "SpeakView");
            clearTimeout(this.recordTimer);
        }

        scrollToLastWord() {
            var $el = $("#textContainer span").last();
            if (!$el.length) {
                return;
            }
            $el.clearQueue();
            $el.stop();

            var offsetTop = $el.offset().top - this.$textContainer.offset().top,
                scrollTop = this.$textContainer.scrollTop(),
                height = this.$textContainer.height();

            if ((offsetTop > height - 30) || (offsetTop < 5)) {
                this.$textContainer.animate({scrollTop: scrollTop + offsetTop - 3}, 500);
            }
        }

        error(msg, err) {
            var div = $("<div>")
                .addClass("alert alert-danger")
                .html(msg);

            this.$app.html(div);
            this.hideOverlay();
        }

        render() {
            this.hideOverlay();
        }
    }

    return SpeakView;
});
